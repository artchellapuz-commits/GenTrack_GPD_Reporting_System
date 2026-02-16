# 📹 Video Integration Guide

## How to Add Video to the Landing Page

The video section is now ready to accept video content. Here are your options:

---

## Option 1: YouTube Video (Recommended)

### Steps:
1. Upload your video to YouTube
2. Get the embed URL:
   - Go to your video on YouTube
   - Click "Share" → "Embed"
   - Copy the URL from `src="..."` (looks like: `https://www.youtube.com/embed/VIDEO_ID`)

3. Update `LandingPage.vue`:
```javascript
data() {
  return {
    videoUrl: 'https://www.youtube.com/embed/YOUR_VIDEO_ID',
    useYouTube: true,
    // ... rest of data
  }
}
```

### Example:
```javascript
videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
useYouTube: true,
```

---

## Option 2: Vimeo Video

### Steps:
1. Upload your video to Vimeo
2. Get the embed URL:
   - Go to your video on Vimeo
   - Click the "Share" button
   - Copy the embed URL (looks like: `https://player.vimeo.com/video/VIDEO_ID`)

3. Update `LandingPage.vue`:
```javascript
data() {
  return {
    videoUrl: 'https://player.vimeo.com/video/YOUR_VIDEO_ID',
    useYouTube: true, // Keep true for iframe embeds
    // ... rest of data
  }
}
```

---

## Option 3: Local Video File

### Steps:
1. Place your video file in `frontend/public/videos/` folder:
   ```
   frontend/
   └── public/
       └── videos/
           └── demo.mp4
   ```

2. Update `LandingPage.vue`:
```javascript
data() {
  return {
    videoUrl: '/videos/demo.mp4',
    useYouTube: false,
    // ... rest of data
  }
}
```

### Supported Formats:
- MP4 (H.264) - Best compatibility
- WebM - Modern browsers
- OGG - Firefox support

### Recommended Settings:
- Resolution: 1920x1080 (Full HD)
- Bitrate: 5-8 Mbps
- Frame Rate: 30 fps
- Audio: AAC, 128-192 kbps

---

## Option 4: External CDN/Cloud Storage

### Steps:
1. Upload video to cloud storage (AWS S3, Google Cloud, Azure, etc.)
2. Get the public URL
3. Update `LandingPage.vue`:

```javascript
data() {
  return {
    videoUrl: 'https://your-cdn.com/path/to/video.mp4',
    useYouTube: false,
    // ... rest of data
  }
}
```

---

## Creating a Demo Video

### What to Include:
1. **Introduction (0:00-0:15)**
   - NPC logo and system name
   - Brief tagline

2. **Dashboard Overview (0:15-0:45)**
   - Show the main dashboard
   - Highlight key metrics
   - Demonstrate real-time updates

3. **Upload Feature (0:45-1:15)**
   - Show drag-and-drop upload
   - File validation
   - Success message

4. **View Reports (1:15-1:45)**
   - Browse historical data
   - Filter by date/plant
   - Show data visualization

5. **Generate Reports (1:45-2:15)**
   - Select date range
   - Choose plants
   - Export to Excel

6. **Comparison Feature (2:15-2:45)**
   - Select multiple plants
   - View side-by-side comparison
   - Show charts

7. **Mobile View (2:45-3:15)**
   - Show responsive design
   - Touch interactions
   - Mobile navigation

8. **Closing (3:15-3:45)**
   - Call to action
   - Contact information
   - NPC branding

### Recording Tools:
- **Windows**: OBS Studio (Free), Camtasia
- **Mac**: QuickTime, ScreenFlow, Camtasia
- **Online**: Loom, Screencast-O-Matic

### Editing Tools:
- **Free**: DaVinci Resolve, OpenShot, Shotcut
- **Paid**: Adobe Premiere Pro, Final Cut Pro

---

## Video Thumbnail

The current thumbnail shows a play button. To customize:

1. Create a custom thumbnail image (1920x1080)
2. Save it in `frontend/public/images/video-thumbnail.jpg`
3. Update the video section in `LandingPage.vue`:

```vue
<div class="video-thumbnail" :style="{ backgroundImage: 'url(/images/video-thumbnail.jpg)' }">
  <div class="video-play-button">
    <i class="pi pi-play"></i>
  </div>
</div>
```

---

## Testing Your Video

### Checklist:
- [ ] Video loads without errors
- [ ] Play button works
- [ ] Video plays smoothly
- [ ] Audio is clear
- [ ] Controls are accessible
- [ ] Modal opens/closes properly
- [ ] Responsive on mobile
- [ ] Works in all browsers (Chrome, Firefox, Safari, Edge)

### Browser Testing:
```bash
# Test in different browsers
- Chrome/Edge (Chromium)
- Firefox
- Safari (Mac/iOS)
- Mobile browsers
```

---

## Performance Optimization

### For Local Videos:
1. **Compress your video**:
   - Use HandBrake or FFmpeg
   - Target: 5-8 Mbps bitrate
   - H.264 codec

2. **Create multiple formats**:
```html
<video controls>
  <source src="/videos/demo.mp4" type="video/mp4">
  <source src="/videos/demo.webm" type="video/webm">
  Your browser does not support the video tag.
</video>
```

3. **Add poster image**:
```html
<video controls poster="/images/video-poster.jpg">
  <source src="/videos/demo.mp4" type="video/mp4">
</video>
```

### For YouTube/Vimeo:
- Videos are automatically optimized
- Adaptive streaming included
- CDN delivery worldwide

---

## Advanced Features

### Auto-play on Modal Open:
```javascript
openVideoModal() {
  this.showVideoModal = true;
  document.body.style.overflow = 'hidden';
  
  // Auto-play video
  this.$nextTick(() => {
    const video = this.$el.querySelector('video');
    if (video) {
      video.play();
    }
  });
}
```

### Track Video Analytics:
```javascript
// Add to mounted()
const video = this.$el.querySelector('video');
if (video) {
  video.addEventListener('play', () => {
    console.log('Video started');
    // Send to analytics
  });
  
  video.addEventListener('ended', () => {
    console.log('Video completed');
    // Send to analytics
  });
}
```

---

## Quick Start Examples

### Example 1: YouTube Video
```javascript
// In LandingPage.vue data()
videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
useYouTube: true,
```

### Example 2: Local MP4
```javascript
// In LandingPage.vue data()
videoUrl: '/videos/npc-demo.mp4',
useYouTube: false,
```

### Example 3: Vimeo
```javascript
// In LandingPage.vue data()
videoUrl: 'https://player.vimeo.com/video/123456789',
useYouTube: true,
```

---

## Troubleshooting

### Video Not Playing:
1. Check file path is correct
2. Verify file format is supported
3. Check browser console for errors
4. Ensure file is in `public` folder

### Video Too Large:
1. Compress using HandBrake
2. Use cloud hosting (YouTube/Vimeo)
3. Use CDN for delivery

### Autoplay Not Working:
- Browsers block autoplay with sound
- Use `muted` attribute for autoplay
- Or require user interaction (click play button)

---

## Current Implementation

The video section is located in `LandingPage.vue`:

**Location**: Line ~180-200 (Video Demo Section)

**Current State**:
- ✅ Video player ready
- ✅ Modal functionality working
- ✅ YouTube/Vimeo support
- ✅ Local video support
- ✅ Responsive design
- ⏳ Waiting for video URL

**To Activate**:
Simply add your video URL to the `videoUrl` data property!

---

## Need Help?

If you need assistance:
1. Recording the video
2. Editing the content
3. Hosting the video
4. Integrating advanced features

Let me know and I can provide more specific guidance!
