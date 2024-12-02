document.addEventListener('DOMContentLoaded', () => {
    const playlistList = document.getElementById('playlist-list');
    const createPlaylistForm = document.getElementById('create-playlist-form');
    const playlistNameInput = document.getElementById('playlist-name');
    const playlistDescriptionInput = document.getElementById('playlist-description');
    const backendUrl = "http://127.0.0.1:8000";

    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const userId = urlParams.get('user_id');

    if (code) {
        // Handle callback and send code to backend for processing
        fetch(`${backendUrl}/callback?code=${code}`)
            .then(response => response.json())
            .then(data => {
                console.log('Login successful:', data);
                const redirectUrl = `${window.location.origin}/frontend?user_id=${data.user_id}`;
                window.location.href = redirectUrl; // Redirect to frontend with user_id
            })
            .catch(err => console.error('Error during callback:', err));
    } else if (!userId) {
        // Initiate login flow if user_id is not present
        fetch(`${backendUrl}/login`)
            .then(response => response.json())
            .then(data => {
                console.log('Redirecting to login:', data.loginUrl);
                window.location.href = data.loginUrl; // Redirect to Spotify login
            })
            .catch(err => console.error('Error initiating login:', err));
    } else {
        // User is logged in, proceed to fetch and display playlist
        console.log(`User ID: ${userId}`);
        fetchPlaylist();
    }

    function fetchPlaylist() {
        fetch(`${backendUrl}/playlist`)
            .then(response => response.json())
            .then(data => {
                playlistList.innerHTML = ''; // Clear existing list
                if (data.playlist && typeof data.playlist === 'object') {
                    // Iterate over each song in the playlist dictionary
                    for (const trackId in data.playlist) {
                        const songData = data.playlist[trackId]; // {user_id: ..., votes: ...}
    
                        // Assuming you have a way to get the song's name and artist
                        const songName = `Song Name for ${trackId}`;  // Replace with actual data
                        const songArtist = `Artist for ${trackId}`;  // Replace with actual data
    
                        const li = document.createElement('li');
                        li.textContent = `${songName} by ${songArtist} - Votes: ${songData.votes}`;
                        const voteButton = createVoteButton(trackId);  // Use trackId here
                        li.appendChild(voteButton);
                        playlistList.appendChild(li);
                    }
                } else {
                    console.error('Expected playlist to be an object:', data.playlist);
                }
            })
            .catch(err => console.error('Error fetching playlist:', err));
    }
    
    

    // Create a new remote playlist
    if (createPlaylistForm) {
        createPlaylistForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const playlistData = {
                name: playlistNameInput.value,
                description: playlistDescriptionInput.value,
                user_id: userId // Include user_id in the request
            };

            fetch(`${backendUrl}/create_playlist`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(playlistData)
            })
                .then(response => response.json())
                .then(data => {
                    alert('Remote playlist created!');
                    playlistNameInput.value = '';
                    playlistDescriptionInput.value = '';
                    fetchPlaylist(userId); // Refresh the playlist
                })
                .catch(err => console.error('Error creating playlist:', err));
        });
    }

    // Create vote button
    function createVoteButton(trackId) {
        const voteButton = document.createElement('button');
        voteButton.textContent = 'Vote';
        voteButton.addEventListener('click', () => {
            fetch(`${backendUrl}/upvote/${trackId}`, {
                method: 'POST'
            })
                .then(response => response.json())
                .then(data => {
                    alert('Song upvoted!');
                    fetchPlaylist(userId); // Refresh the playlist
                })
                .catch(err => console.error('Error voting on song:', err));
        });
        return voteButton;
    }
});
