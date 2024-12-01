document.addEventListener('DOMContentLoaded', () => {
    const playlistList = document.getElementById('playlist-list');
    const createPlaylistForm = document.getElementById('create-playlist-form');
    const playlistNameInput = document.getElementById('playlist-name');
    const playlistDescriptionInput = document.getElementById('playlist-description');
    const songList = document.getElementById('song-list');
    const userId = 'user-id'; // Replace with actual user ID
    const backendUrl = "http://127.0.0.1:8000"; 

    fetch(`${backendUrl}/login`)  // todo: need to make sure we redirect correctlly
    .then(response => response.json())
    .then(data => {
        // Redirect the user to the login URL
        window.location.href = data.loginUrl;
    });

    // Fetch current playlist
    fetch(`${backendUrl}/playlist`)  // todo: need to make it on commend and not immediately 
        .then(response => response.json())
        .then(data => {
            data.playlist.forEach(song => {
                const li = document.createElement('li');
                li.textContent = `${song.name} by ${song.artist}`;
                const voteButton = createVoteButton(song.id);
                li.appendChild(voteButton);
                playlistList.appendChild(li);
            });
        });

    // Create a new playlist
    createPlaylistForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const playlistData = {
            name: playlistNameInput.value,
            description: playlistDescriptionInput.value
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
        });
    });

    // Upvote a song
    function createVoteButton(trackId) {
        const voteButton = document.createElement('button');
        voteButton.textContent = 'Vote';
        voteButton.addEventListener('click', () => {
            fetch(`/upvote/${trackId}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                alert('Song upvoted!');
            });
        });
        return voteButton;
    }

    // Fetch next song in playlist
    function getNextSong() {
        fetch(`${backendUrl}/next_song`)
            .then(response => response.json())
            .then(data => {
                alert(`Next song: ${data['The next song is:']} with ${data.votes} votes.`);
            });
    }

    // Fetch user data
    fetch(`${backendUrl}/user/${userId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data.user_data); // Display user data as needed
        });
});
