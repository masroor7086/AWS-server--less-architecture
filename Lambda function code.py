import boto3
import json
from urllib.parse import unquote_plus

def lambda_handler(event, context):
    config = {
        'S3_BUCKET': 'masroor-streaming',
        'PRESIGNED_URL_EXPIRY': 3600,
        'VIDEO_LIBRARY': [
            {
                'title': 'Unforgettable Choo Lo Mashup 2.0',
                'filename': 'Unforgettable Choo Lo Mashup 2.0 - Shivendra Singh & Anuv Jain.mp4',
                'category': 'Music',
                'duration': '3:45',
                'views': '12.5K',
                'upload_date': '2023-10-15',
                'description': 'Beautiful mashup of classic and contemporary melodies'
            },
            {
                'title': 'Tera Mera Rishta Purana',
                'filename': 'Tera Mera Rishta Purana (HD) Video Song _ Awarapan Movie Song _ Emraan Hashmi Songs _ Mustafa Zahid.mp4',
                'category': 'Bollywood',
                'duration': '5:22',
                'views': '8.9K',
                'upload_date': '2023-09-28',
                'description': 'Iconic romantic track from the classic movie Awarapan'
            },
            {
                'title': 'Ik Lamha - Azaan Sami Khan',
                'filename': 'Azaan Sami Khan - Ik Lamha ft. Maya Ali (Official Music Video).mp4',
                'category': 'Music',
                'duration': '4:15',
                'views': '15.2K',
                'upload_date': '2023-11-05',
                'description': 'Official music video starring Maya Ali'
            },
            {
                'title': 'ISHQ - Music Film',
                'filename': 'ISHQ - Music Film I Amir Ameer I Faheem Abdullah I Rauhan Malik I Samreen Kaur I Mir Tafazul.mp4',
                'category': 'Short Film',
                'duration': '12:38',
                'views': '21K',
                'upload_date': '2023-08-20',
                'description': 'Award-winning musical short film about love and sacrifice'
            },
            {
                'title': 'Demo Video',
                'filename': 'videoplayback.mp4',
                'category': 'Demo',
                'duration': '2:10',
                'views': '5K',
                'upload_date': '2023-12-01',
                'description': 'Demonstration of our streaming platform capabilities'
            }
        ]
    }

    try:
        # Get requested video
        current_video = config['VIDEO_LIBRARY'][0]
        if 'queryStringParameters' in event and event['queryStringParameters']:
            if 'video' in event['queryStringParameters']:
                requested_video = unquote_plus(event['queryStringParameters']['video'])
                for video in config['VIDEO_LIBRARY']:
                    if video['filename'] == requested_video:
                        current_video = video
                        break

        # Generate presigned URL
        s3_client = boto3.client('s3')
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': config['S3_BUCKET'], 'Key': current_video['filename']},
            ExpiresIn=config['PRESIGNED_URL_EXPIRY']
        )

        # Build HTML
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Masroor Premium Stream</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                :root {{
                    /* Light Theme */
                    --light-primary: #2563eb;
                    --light-primary-dark: #1d4ed8;
                    --light-bg: #f8fafc;
                    --light-card: #ffffff;
                    --light-text: #0f172a;
                    --light-gray: #94a3b8;
                    --light-border: #e2e8f0;
                    
                    /* Dark Theme */
                    --dark-primary: #6366f1;
                    --dark-primary-dark: #4f46e5;
                    --dark-bg: #0f172a;
                    --dark-card: #1e293b;
                    --dark-text: #f8fafc;
                    --dark-gray: #64748b;
                    --dark-border: #334155;
                    
                    /* Active Theme (Defaults to Dark) */
                    --primary: var(--dark-primary);
                    --primary-dark: var(--dark-primary-dark);
                    --bg: var(--dark-bg);
                    --card: var(--dark-card);
                    --text: var(--dark-text);
                    --gray: var(--dark-gray);
                    --border: var(--dark-border);
                }}
                
                [data-theme="light"] {{
                    --primary: var(--light-primary);
                    --primary-dark: var(--light-primary-dark);
                    --bg: var(--light-bg);
                    --card: var(--light-card);
                    --text: var(--light-text);
                    --gray: var(--light-gray);
                    --border: var(--light-border);
                }}
                
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Inter', sans-serif;
                }}
                
                body {{
                    background-color: var(--bg);
                    color: var(--text);
                    min-height: 100vh;
                    transition: all 0.3s ease;
                }}
                
                /* Layout */
                .app-container {{
                    display: grid;
                    grid-template-columns: 240px 1fr;
                    min-height: 100vh;
                }}
                
                /* Sidebar */
                .sidebar {{
                    background-color: var(--card);
                    border-right: 1px solid var(--border);
                    padding: 20px;
                    position: fixed;
                    width: 240px;
                    height: 100vh;
                    overflow-y: auto;
                    z-index: 100;
                }}
                
                .logo {{
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 1px solid var(--border);
                }}
                
                .logo-icon {{
                    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                    width: 32px;
                    height: 32px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                }}
                
                .logo-text {{
                    font-size: 20px;
                    font-weight: 700;
                }}
                
                .nav-menu {{
                    list-style: none;
                    margin-top: 20px;
                }}
                
                .nav-item {{
                    margin-bottom: 8px;
                }}
                
                .nav-link {{
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    padding: 12px 16px;
                    border-radius: 8px;
                    color: var(--gray);
                    text-decoration: none;
                    font-weight: 500;
                    transition: all 0.2s;
                }}
                
                .nav-link:hover, .nav-link.active {{
                    background-color: rgba(99, 102, 241, 0.1);
                    color: var(--primary);
                }}
                
                .nav-link i {{
                    width: 20px;
                    text-align: center;
                }}
                
                /* Main Content */
                .main-content {{
                    grid-column: 2;
                    padding: 30px;
                    margin-left: 240px;
                }}
                
                .header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 30px;
                }}
                
                .search-bar {{
                    position: relative;
                    width: 400px;
                }}
                
                .search-bar input {{
                    width: 100%;
                    padding: 12px 20px 12px 45px;
                    border-radius: 50px;
                    border: 1px solid var(--border);
                    background-color: var(--card);
                    color: var(--text);
                    font-size: 14px;
                    transition: all 0.3s;
                }}
                
                .search-bar input:focus {{
                    outline: none;
                    border-color: var(--primary);
                    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
                }}
                
                .search-icon {{
                    position: absolute;
                    left: 15px;
                    top: 50%;
                    transform: translateY(-50%);
                    color: var(--gray);
                }}
                
                .user-menu {{
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }}
                
                .btn {{
                    padding: 10px 18px;
                    border-radius: 8px;
                    font-weight: 500;
                    font-size: 14px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    transition: all 0.2s;
                }}
                
                .btn-primary {{
                    background-color: var(--primary);
                    color: white;
                    border: none;
                }}
                
                .btn-primary:hover {{
                    background-color: var(--primary-dark);
                    transform: translateY(-1px);
                }}
                
                .btn-outline {{
                    background-color: transparent;
                    color: var(--primary);
                    border: 1px solid var(--primary);
                }}
                
                .btn-outline:hover {{
                    background-color: rgba(99, 102, 241, 0.1);
                }}
                
                .user-avatar {{
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background-color: var(--primary);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    cursor: pointer;
                }}
                
                /* Video Player Section */
                .video-section {{
                    display: grid;
                    grid-template-columns: 1fr 350px;
                    gap: 30px;
                    margin-bottom: 40px;
                }}
                
                .video-container {{
                    background-color: var(--card);
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                }}
                
                video {{
                    width: 100%;
                    aspect-ratio: 16/9;
                    display: block;
                    background-color: #000;
                }}
                
                .video-controls {{
                    padding: 20px;
                }}
                
                .video-title {{
                    font-size: 22px;
                    font-weight: 700;
                    margin-bottom: 12px;
                }}
                
                .video-meta {{
                    display: flex;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 15px;
                    margin-bottom: 20px;
                    color: var(--gray);
                    font-size: 14px;
                }}
                
                .video-meta span {{
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }}
                
                .video-actions {{
                    display: flex;
                    gap: 12px;
                    margin-bottom: 20px;
                }}
                
                .video-description {{
                    background-color: rgba(99, 102, 241, 0.05);
                    padding: 16px;
                    border-radius: 8px;
                    font-size: 14px;
                    line-height: 1.6;
                    color: var(--text);
                    border: 1px solid var(--border);
                }}
                
                /* Playlist Section */
                .playlist-container {{
                    background-color: var(--card);
                    border-radius: 12px;
                    padding: 20px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                    height: calc(100vh - 200px);
                    overflow-y: auto;
                }}
                
                .section-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                }}
                
                .section-title {{
                    font-size: 18px;
                    font-weight: 700;
                }}
                
                .section-count {{
                    background-color: var(--primary);
                    color: white;
                    padding: 2px 8px;
                    border-radius: 50px;
                    font-size: 12px;
                }}
                
                .playlist-search {{
                    position: relative;
                    margin-bottom: 15px;
                }}
                
                .playlist-search input {{
                    width: 100%;
                    padding: 10px 15px 10px 40px;
                    border-radius: 8px;
                    border: 1px solid var(--border);
                    background-color: var(--bg);
                    color: var(--text);
                    font-size: 14px;
                }}
                
                .playlist-search i {{
                    position: absolute;
                    left: 15px;
                    top: 50%;
                    transform: translateY(-50%);
                    color: var(--gray);
                }}
                
                .video-list {{
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }}
                
                .video-item {{
                    display: flex;
                    gap: 15px;
                    padding: 12px;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: all 0.2s;
                    background-color: var(--bg);
                }}
                
                .video-item:hover {{
                    background-color: rgba(99, 102, 241, 0.1);
                }}
                
                .video-item.active {{
                    background-color: rgba(99, 102, 241, 0.2);
                    border-left: 3px solid var(--primary);
                }}
                
                .video-thumb {{
                    width: 120px;
                    height: 68px;
                    border-radius: 6px;
                    background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 24px;
                    flex-shrink: 0;
                }}
                
                .video-details {{
                    flex: 1;
                    overflow: hidden;
                }}
                
                .video-item-title {{
                    font-size: 14px;
                    font-weight: 600;
                    margin-bottom: 6px;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }}
                
                .video-item-meta {{
                    display: flex;
                    gap: 10px;
                    color: var(--gray);
                    font-size: 12px;
                }}
                
                /* Recommendations Section */
                .recommendations {{
                    margin-top: 40px;
                }}
                
                .video-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                    gap: 20px;
                }}
                
                .video-card {{
                    background-color: var(--card);
                    border-radius: 10px;
                    overflow: hidden;
                    transition: transform 0.3s, box-shadow 0.3s;
                    cursor: pointer;
                }}
                
                .video-card:hover {{
                    transform: translateY(-5px);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
                }}
                
                .card-thumbnail {{
                    width: 100%;
                    aspect-ratio: 16/9;
                    background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 30px;
                }}
                
                .card-body {{
                    padding: 14px;
                }}
                
                .card-title {{
                    font-size: 14px;
                    font-weight: 600;
                    margin-bottom: 8px;
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                }}
                
                .card-meta {{
                    display: flex;
                    justify-content: space-between;
                    color: var(--gray);
                    font-size: 12px;
                }}
                
                /* Theme Toggle */
                .theme-toggle {{
                    position: fixed;
                    bottom: 30px;
                    right: 30px;
                    width: 50px;
                    height: 50px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                    z-index: 1000;
                    border: none;
                    font-size: 20px;
                    transition: transform 0.3s;
                }}
                
                .theme-toggle:hover {{
                    transform: scale(1.1);
                }}
                
                /* Quality Selector */
                .quality-selector {{
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-top: 10px;
                }}
                
                .quality-selector select {{
                    padding: 8px 12px;
                    border-radius: 6px;
                    border: 1px solid var(--border);
                    background-color: var(--bg);
                    color: var(--text);
                    font-size: 14px;
                }}
                
                /* PIP Button */
                .pip-btn {{
                    position: absolute;
                    bottom: 20px;
                    right: 20px;
                    background-color: rgba(0, 0, 0, 0.7);
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    z-index: 10;
                }}
                
                /* Progress Bar */
                .progress-container {{
                    height: 4px;
                    background-color: rgba(255, 255, 255, 0.1);
                    width: 100%;
                }}
                
                .progress-bar {{
                    height: 100%;
                    background-color: var(--primary);
                    width: 0%;
                    transition: width 0.1s;
                }}
                
                /* Keyboard Shortcuts Panel */
                .shortcuts-panel {{
                    position: fixed;
                    bottom: 100px;
                    right: 30px;
                    background-color: var(--card);
                    padding: 15px;
                    border-radius: 12px;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                    z-index: 1000;
                    width: 220px;
                    display: none;
                }}
                
                .shortcuts-panel.show {{
                    display: block;
                    animation: fadeIn 0.3s;
                }}
                
                .shortcuts-header {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 12px;
                }}
                
                .shortcuts-title {{
                    font-size: 16px;
                    font-weight: 600;
                }}
                
                .shortcut-item {{
                    display: flex;
                    justify-content: space-between;
                    padding: 8px 0;
                    border-bottom: 1px solid var(--border);
                }}
                
                .shortcut-key {{
                    background-color: var(--bg);
                    padding: 3px 8px;
                    border-radius: 4px;
                    font-family: monospace;
                }}
                
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(10px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                
                /* Responsive Design */
                @media (max-width: 1200px) {{
                    .video-section {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .playlist-container {{
                        height: auto;
                        max-height: 400px;
                    }}
                }}
                
                @media (max-width: 768px) {{
                    .app-container {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .sidebar {{
                        width: 100%;
                        height: auto;
                        position: relative;
                        padding: 15px;
                    }}
                    
                    .main-content {{
                        margin-left: 0;
                        padding: 20px;
                    }}
                    
                    .header {{
                        flex-direction: column;
                        gap: 15px;
                    }}
                    
                    .search-bar {{
                        width: 100%;
                    }}
                    
                    .user-menu {{
                        width: 100%;
                        justify-content: space-between;
                    }}
                }}
                
                @media (max-width: 576px) {{
                    .video-actions {{
                        flex-wrap: wrap;
                    }}
                    
                    .video-grid {{
                        grid-template-columns: 1fr;
                    }}
                }}
            </style>
        </head>
        <body data-theme="dark">
            <div class="app-container">
                <!-- Sidebar Navigation -->
                <nav class="sidebar">
                    <div class="logo">
                        <div class="logo-icon">
                            <i class="fas fa-play"></i>
                        </div>
                        <div class="logo-text">Masroor Stream</div>
                    </div>
                    
                    <ul class="nav-menu">
                        <li class="nav-item">
                            <a href="#" class="nav-link active">
                                <i class="fas fa-home"></i>
                                <span>Home</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link">
                                <i class="fas fa-compass"></i>
                                <span>Explore</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link">
                                <i class="fas fa-clock"></i>
                                <span>Watch Later</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link">
                                <i class="fas fa-history"></i>
                                <span>History</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link">
                                <i class="fas fa-download"></i>
                                <span>Downloads</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="#" class="nav-link">
                                <i class="fas fa-cog"></i>
                                <span>Settings</span>
                            </a>
                        </li>
                    </ul>
                </nav>
                
                <!-- Main Content -->
                <main class="main-content">
                    <header class="header">
                        <div class="search-bar">
                            <i class="fas fa-search search-icon"></i>
                            <input type="text" placeholder="Search videos, categories...">
                        </div>
                        
                        <div class="user-menu">
                            <button class="btn btn-outline" onclick="showShortcuts()">
                                <i class="fas fa-keyboard"></i> Shortcuts
                            </button>
                            <button class="btn btn-primary">
                                <i class="fas fa-upload"></i> Upload
                            </button>
                            <div class="user-avatar">
                                <i class="fas fa-user"></i>
                            </div>
                        </div>
                    </header>
                    
                    <!-- Video Section -->
                    <section class="video-section">
                        <div class="video-container">
                            <video controls autoplay id="main-video">
                                <source src="{presigned_url}" type="video/mp4">
                                Your browser doesn't support HTML5 video.
                            </video>
                            <div class="progress-container">
                                <div class="progress-bar"></div>
                            </div>
                            
                            <button class="pip-btn" onclick="togglePIP()">
                                <i class="fas fa-clone"></i> PIP Mode
                            </button>
                            
                            <div class="video-controls">
                                <h1 class="video-title">{current_video['title']}</h1>
                                
                                <div class="video-meta">
                                    <span><i class="fas fa-eye"></i> {current_video['views']} views</span>
                                    <span><i class="fas fa-clock"></i> {current_video['duration']}</span>
                                    <span><i class="fas fa-calendar"></i> {current_video['upload_date']}</span>
                                    <span><i class="fas fa-tag"></i> {current_video['category']}</span>
                                </div>
                                
                                <div class="quality-selector">
                                    <span>Quality:</span>
                                    <select onchange="changeQuality(this.value)">
                                        <option value="1080">1080p (HD)</option>
                                        <option value="720" selected>720p (SD)</option>
                                        <option value="480">480p</option>
                                    </select>
                                </div>
                                
                                <div class="video-actions">
                                    <button class="btn btn-primary">
                                        <i class="fas fa-thumbs-up"></i> Like
                                    </button>
                                    <button class="btn btn-outline">
                                        <i class="fas fa-share"></i> Share
                                    </button>
                                    <button class="btn btn-outline" onclick="addToWatchLater('{current_video['filename']}')">
                                        <i class="fas fa-clock"></i> Watch Later
                                    </button>
                                </div>
                                
                                <div class="video-description">
                                    <p>{current_video['description']}</p>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Playlist Section -->
                        <div class="playlist-container">
                            <div class="section-header">
                                <h2 class="section-title">Playlist</h2>
                                <span class="section-count">{len(config['VIDEO_LIBRARY'])}</span>
                            </div>
                            
                            <div class="playlist-search">
                                <i class="fas fa-search"></i>
                                <input type="text" id="search-input" placeholder="Search in playlist...">
                            </div>
                            
                            <div class="video-list">
                                {''.join(
                                    f'<div class="video-item {"active" if video["filename"] == current_video["filename"] else ""}" '
                                    f'data-title="{video["title"]}" '
                                    f'onclick="window.location.href=\'?video={video["filename"]}\'">'
                                    f'<div class="video-thumb"><i class="fas fa-play"></i></div>'
                                    f'<div class="video-details">'
                                    f'<h3 class="video-item-title">{video["title"]}</h3>'
                                    f'<div class="video-item-meta">'
                                    f'<span>{video["duration"]}</span>'
                                    f'<span>{video["views"]} views</span>'
                                    f'</div></div></div>'
                                    for video in config['VIDEO_LIBRARY']
                                )}
                            </div>
                        </div>
                    </section>
                    
                    <!-- Recommendations Section -->
                    <section class="recommendations">
                        <div class="section-header">
                            <h2 class="section-title">Recommended For You</h2>
                            <a href="#" style="color: var(--primary); font-size: 14px;">See All</a>
                        </div>
                        
                        <div class="video-grid">
                            {''.join(
                                f'<div class="video-card" onclick="window.location.href=\'?video={video["filename"]}\'">'
                                f'<div class="card-thumbnail"><i class="fas fa-play"></i></div>'
                                f'<div class="card-body">'
                                f'<h3 class="card-title">{video["title"]}</h3>'
                                f'<div class="card-meta">'
                                f'<span>{video["views"]}</span>'
                                f'<span>{video["duration"]}</span>'
                                f'</div></div></div>'
                                for video in sorted(config['VIDEO_LIBRARY'], key=lambda x: x['views'], reverse=True)[:4]
                            )}
                        </div>
                    </section>
                </main>
            </div>
            
            <!-- Theme Toggle Button -->
            <button class="theme-toggle" onclick="toggleTheme()">
                <i class="fas fa-moon"></i>
            </button>
            
            <!-- Keyboard Shortcuts Panel -->
            <div class="shortcuts-panel" id="shortcuts-panel">
                <div class="shortcuts-header">
                    <h3 class="shortcuts-title">Keyboard Shortcuts</h3>
                    <button onclick="hideShortcuts()" style="background: none; border: none; color: var(--gray); cursor: pointer;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <div class="shortcut-item">
                    <span>Play/Pause</span>
                    <span class="shortcut-key">Space</span>
                </div>
                <div class="shortcut-item">
                    <span>Mute</span>
                    <span class="shortcut-key">M</span>
                </div>
                <div class="shortcut-item">
                    <span>Fullscreen</span>
                    <span class="shortcut-key">F</span>
                </div>
                <div class="shortcut-item">
                    <span>Seek Forward</span>
                    <span class="shortcut-key">→</span>
                </div>
                <div class="shortcut-item">
                    <span>Seek Backward</span>
                    <span class="shortcut-key">←</span>
                </div>
                <div class="shortcut-item">
                    <span>Like Video</span>
                    <span class="shortcut-key">L</span>
                </div>
            </div>
            
            <script>
                // Enhanced JavaScript with all features
                document.addEventListener('DOMContentLoaded', function() {{
                    // Playlist search functionality
                    document.getElementById('search-input').addEventListener('input', function(e) {{
                        const searchTerm = e.target.value.toLowerCase();
                        document.querySelectorAll('.video-item').forEach(item => {{
                            const title = item.dataset.title.toLowerCase();
                            item.style.display = title.includes(searchTerm) ? 'flex' : 'none';
                        }});
                    }});
                    
                    // Video progress tracking
                    const video = document.querySelector('#main-video');
                    if (video) {{
                        video.addEventListener('timeupdate', function() {{
                            const percent = (video.currentTime / video.duration) * 100;
                            document.querySelector('.progress-bar').style.width = percent + '%';
                        }});
                    }}
                    
                    // Watch Later functionality
                    window.addToWatchLater = function(videoId) {{
                        let playlist = JSON.parse(localStorage.getItem('watchLater') || '[]');
                        if (!playlist.includes(videoId)) {{
                            playlist.push(videoId);
                            localStorage.setItem('watchLater', JSON.stringify(playlist));
                            alert('Added to Watch Later!');
                        }}
                    }};
                    
                    // Quality selector (simulated)
                    window.changeQuality = function(quality) {{
                        console.log('Quality changed to', quality);
                        // In a real app, you'd switch video sources here
                    }};
                    
                    // PIP Mode
                    window.togglePIP = async function() {{
                        const video = document.querySelector('#main-video');
                        try {{
                            if (document.pictureInPictureElement) {{
                                await document.exitPictureInPicture();
                            }} else if (document.pictureInPictureEnabled) {{
                                await video.requestPictureInPicture();
                            }}
                        }} catch (err) {{
                            console.error('PIP error:', err);
                        }}
                    }};
                    
                    // Theme toggle
                    window.toggleTheme = function() {{
                        const newTheme = document.body.dataset.theme === 'dark' ? 'light' : 'dark';
                        document.body.dataset.theme = newTheme;
                        
                        // Update theme toggle icon
                        const icon = document.querySelector('.theme-toggle i');
                        icon.className = newTheme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
                    }};
                    
                    // Keyboard shortcuts
                    document.addEventListener('keydown', (e) => {{
                        const video = document.querySelector('#main-video');
                        if (!video) return;
                        
                        switch (e.key) {{
                            case ' ':
                                e.preventDefault();
                                video.paused ? video.play() : video.pause();
                                break;
                            case 'm':
                                video.muted = !video.muted;
                                break;
                            case 'f':
                                if (video.requestFullscreen) {{
                                    video.requestFullscreen();
                                }} else if (video.webkitRequestFullscreen) {{
                                    video.webkitRequestFullscreen();
                                }}
                                break;
                            case 'ArrowRight':
                                video.currentTime += 5;
                                break;
                            case 'ArrowLeft':
                                video.currentTime -= 5;
                                break;
                            case 'l':
                                document.querySelector('.btn-primary').click();
                                break;
                        }}
                    }});
                    
                    // Show/hide keyboard shortcuts
                    window.showShortcuts = function() {{
                        document.getElementById('shortcuts-panel').classList.add('show');
                    }};
                    
                    window.hideShortcuts = function() {{
                        document.getElementById('shortcuts-panel').classList.remove('show');
                    }};
                }});
            </script>
        </body>
        </html>
        """

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }