document.addEventListener('DOMContentLoaded', () => {
    // Basic setup
    const API_BASE_URL = 'http://127.0.0.1:8000';
    
    // Get DOM elements
    const loginBtn = document.getElementById('loginBtn');
    const userSection = document.getElementById('userSection');
    const playlistContainer = document.getElementById('playlistContainer');
    
    // Add login click handler
    if (loginBtn) {
        loginBtn.addEventListener('click', async () => {
            console.log('Login clicked');
            try {
                const response = await fetch(`${API_BASE_URL}/login`);
                const data = await response.json();
                console.log('Received login URL:', data.url);
                window.location.href = data.url;
            } catch (error) {
                console.error('Error during login:', error);
            }
        });
    }

    // Check if we're logged in
    const urlParams = new URLSearchParams(window.location.search);
    const userId = urlParams.get('user_id');
    console.log('User ID from URL:', userId);

    if (userId) {
        // User is logged in, show playlist controls
        loginBtn.style.display = 'none';
        userSection.innerHTML += `
            <button id="generateBtn" class="primary-btn">Generate Playlist</button>
        `;

        // Add generate button handler
        const generateBtn = document.getElementById('generateBtn');
        generateBtn.addEventListener('click', async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/generate_playlist`, {
                    method: 'POST'
                });
                if (response.ok) {
                    updatePlaylist();
                }
            } catch (error) {
                console.error('Error generating playlist:', error);
            }
        });

        // Initial playlist load
        updatePlaylist();
    }

    async function updatePlaylist() {
        try {
            const response = await fetch(`${API_BASE_URL}/playlist`);
            const data = await response.json();
            console.log('Playlist data:', data);
            displayPlaylist(data.playlist || {});
        } catch (error) {
            console.error('Error fetching playlist:', error);
        }
    }

    function displayPlaylist(playlist) {
        if (!playlistContainer) return;

        playlistContainer.innerHTML = '';
        
        // Use the playlist directly since it's already sorted
        Object.entries(playlist).forEach(([trackId, song]) => {
            const songElement = document.createElement('div');
            songElement.className = 'song-card';
            songElement.innerHTML = `
                <div class="song-info">
                    <div class="song-title">${song.name}</div>
                    <div class="song-artist">${song.artist}</div>
                </div>
                <div class="vote-section">
                    <span class="vote-count">${song.votes} votes</span>
                    <button class="vote-btn" onclick="upvoteSong('${trackId}')">
                        Upvote
                    </button>
                </div>
            `;
            playlistContainer.appendChild(songElement);
        });
    }

    // Global function for upvoting
    window.upvoteSong = async (trackId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/upvote/${trackId}`, {
                method: 'PUT'
            });
            if (response.ok) {
                updatePlaylist();
            }
        } catch (error) {
            console.error('Error upvoting song:', error);
        }
    };
});

