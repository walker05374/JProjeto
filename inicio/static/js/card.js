
    const videoPlayerCard = document.getElementById('video-player-card');

    if (videoPlayerCard) {
        const videoId = videoPlayerCard.dataset.videoId;
        const thumbnailUrl = `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`;
        videoPlayerCard.style.backgroundImage = `url('${thumbnailUrl}')`;
    }
