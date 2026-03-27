<template>
  <div class="landing-page" :class="{ 'dark-mode': darkMode }">
    <!-- Scroll Progress Indicator -->
    <div class="scroll-progress-bar" :style="{ width: scrollProgress + '%' }"></div>
    
    <!-- Theme Controls -->
    <ThemeControls />

    <!-- Hero Section -->
    <section id="hero" class="hero-section">
      <div class="hero-background-container">
        <!-- Modern Mesh Gradient Background -->
        <div class="mesh-gradient-bg"></div>
        
        <!-- Animated Energy Particles -->
        <div class="energy-particles">
          <div v-for="n in 15" :key="n" class="energy-particle" :style="generateParticleStyle(n)"></div>
        </div>
        
        <!-- Subtle Texture Overlay -->
        <div class="grain-overlay"></div>
        
        <!-- Animated Data Grid Overlay -->
        <div class="data-grid-overlay"></div>
        
        <!-- Floating Accent Orbs -->
        <div class="accent-orbs">
          <div class="accent-orb accent-orb-1"></div>
          <div class="accent-orb accent-orb-2"></div>
          <div class="accent-orb accent-orb-3"></div>
        </div>
        
        <!-- Animated UI Mockup -->
        <div class="ui-mockup-container">
          <div class="ui-mockup">
            <div class="mockup-header">
              <div class="mockup-dot"></div>
              <div class="mockup-dot"></div>
              <div class="mockup-dot"></div>
            </div>
            <div class="mockup-body">
              <div class="mockup-sidebar"></div>
              <div class="mockup-content">
                <div class="mockup-row"></div>
                <div class="mockup-row"></div>
                <div class="mockup-row"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="hero-overlay"></div>
      <div class="container">
        <div class="hero-content">
            <div class="logo-hero">
              <!-- Animated SVG Logo for GenTrack -->
              <div class="gentrack-logo hero-logo-svg">
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                  <!-- Background Hexagon -->
                  <polygon points="50,5 90,27.5 90,72.5 50,95 10,72.5 10,27.5" fill="none" stroke="#3b82f6" stroke-width="6" class="logo-hex"/>
                  
                  <!-- Power Lightning Bolt -->
                  <path d="M55,20 L35,55 L50,55 L45,80 L65,45 L50,45 Z" fill="#60a5fa" class="logo-bolt"/>
                  
                  <!-- Data Connection Nodes -->
                  <circle cx="35" cy="55" r="4" fill="#fb923c" class="logo-node"/>
                  <circle cx="50" cy="55" r="4" fill="#fb923c" class="logo-node"/>
                  <circle cx="65" cy="45" r="4" fill="#fb923c" class="logo-node"/>
                  <circle cx="50" cy="45" r="4" fill="#fb923c" class="logo-node"/>
                </svg>
              </div>
            </div>
            <h1 class="hero-title">GenTrack</h1>
            <p class="hero-subtitle">Generation and Performance Division - Agus-Pulangi Hydro-Electric Power Plants</p>
            <p class="hero-tagline">Streamline your power generation reporting with real-time analytics</p>
            
            <div class="cta-buttons">
              <router-link to="/login" class="btn btn-primary">
                <i class="pi pi-sign-in"></i>
                Sign In
              </router-link>
            </div>
        </div>
      </div>
      
      <!-- Animated Scroll Hint -->
      <div class="scroll-hint" @click="scrollToFeatures">
        <div class="mouse">
          <div class="wheel"></div>
        </div>
        <div class="arrows">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section">
      <div class="container">
        <h2 class="section-title">Powerful Features</h2>
        <p class="section-subtitle">Everything you need to manage power plant reporting</p>
        
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <i class="pi pi-chart-line"></i>
            </div>
            <h3>Real-time Dashboard</h3>
            <p>Monitor all power plants at a glance with live data visualization and instant updates</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="pi pi-upload"></i>
            </div>
            <h3>Easy Upload</h3>
            <p>Import Excel reports seamlessly with automatic data validation and error checking</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="pi pi-chart-bar"></i>
            </div>
            <h3>Analytics & Charts</h3>
            <p>Visualize generation trends, capacity factors, and performance metrics</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">
              <i class="pi pi-download"></i>
            </div>
            <h3>Export Reports</h3>
            <p>Generate comprehensive reports in multiple formats for easy sharing</p>
          </div>
        </div>
      </div>
    </section>

  

    <!-- Plant Showcase Carousel -->
    <section id="plants" class="plants-carousel-section">
      <div class="container">
        <h2 class="section-title">Our Power Plants</h2>
        <p class="section-subtitle">Explore the 7 hydroelectric power plants in the Agus-Pulangi system</p>
        
        <div class="carousel-container">
          <button @click="prevPlant" class="carousel-btn carousel-btn-prev">
            <i class="pi pi-chevron-left"></i>
          </button>
          
          <div class="carousel-track">
            <div 
              v-for="(plant, index) in powerPlants" 
              :key="plant.code"
              class="carousel-slide"
              :class="{ active: index === currentPlantIndex }"
            >
              <div class="plant-showcase-card">
                <div class="plant-image-placeholder">
                  <i class="pi pi-bolt"></i>
                  <div class="plant-code-overlay">{{ plant.code }}</div>
                </div>
                <div class="plant-showcase-content">
                  <h3>{{ plant.name }}</h3>
                  <div class="plant-details">
                    <div class="plant-detail-item">
                      <i class="pi pi-map-marker"></i>
                      <span>{{ plant.location }}</span>
                    </div>
                    <div class="plant-detail-item">
                      <i class="pi pi-bolt"></i>
                      <span>{{ plant.capacity }} MW</span>
                    </div>
                    <div class="plant-detail-item">
                      <i class="pi pi-cog"></i>
                      <span>{{ plant.units }} Units</span>
                    </div>
                  </div>
                  <p class="plant-description">{{ plant.description }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <button @click="nextPlant" class="carousel-btn carousel-btn-next">
            <i class="pi pi-chevron-right"></i>
          </button>
        </div>
        
        <div class="carousel-indicators">
          <button 
            v-for="(plant, index) in powerPlants" 
            :key="index"
            @click="goToPlant(index)"
            class="carousel-indicator"
            :class="{ active: index === currentPlantIndex }"
          ></button>
        </div>
      </div>
    </section>

    <!-- Live Stats Dashboard -->
    <section id="live-stats" class="live-stats-section">
      <div class="container">
        <h2 class="section-title">Live System Statistics</h2>
        <p class="section-subtitle">Real-time monitoring of the GenTrack</p>
        
        <div class="live-stats-grid">
          <div class="live-stat-card">
            <div class="live-stat-icon">
              <i class="pi pi-users"></i>
            </div>
            <div class="live-stat-content">
              <div class="live-stat-value">{{ liveStats.activeUsers }}</div>
              <div class="live-stat-label">Active Users</div>
              <div class="live-stat-trend positive">
                <i class="pi pi-arrow-up"></i> +12% today
              </div>
            </div>
          </div>
          
          <div class="live-stat-card">
            <div class="live-stat-icon">
              <i class="pi pi-file"></i>
            </div>
            <div class="live-stat-content">
              <div class="live-stat-value">{{ liveStats.reportsProcessed.toLocaleString() }}</div>
              <div class="live-stat-label">Reports Processed</div>
              <div class="live-stat-trend positive">
                <i class="pi pi-arrow-up"></i> +245 this week
              </div>
            </div>
          </div>
          
          <div class="live-stat-card">
            <div class="live-stat-icon">
              <i class="pi pi-check-circle"></i>
            </div>
            <div class="live-stat-content">
              <div class="live-stat-value">{{ liveStats.uptime }}%</div>
              <div class="live-stat-label">System Uptime</div>
              <div class="live-stat-trend positive">
                <i class="pi pi-check"></i> All systems operational
              </div>
            </div>
          </div>
          
          <div class="live-stat-card">
            <div class="live-stat-icon">
              <i class="pi pi-clock"></i>
            </div>
            <div class="live-stat-content">
              <div class="live-stat-value">{{ liveStats.avgResponseTime }}ms</div>
              <div class="live-stat-label">Avg Response Time</div>
              <div class="live-stat-trend positive">
                <i class="pi pi-arrow-down"></i> -15ms improved
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Carousel -->
    <section id="testimonials" class="testimonials-section">
      <div class="container">
        <h2 class="section-title">What Our Users Say</h2>
        <p class="section-subtitle">Trusted by GPD personnel across all power plants</p>
        
        <div class="feedback-cta">
          <button @click="showFeedbackModal = true" class="btn-feedback">
            <i class="pi pi-star"></i>
            Share Your Experience
          </button>
        </div>
        
        <div class="testimonials-carousel">
          <button @click="prevTestimonial" class="testimonial-btn testimonial-btn-prev">
            <i class="pi pi-chevron-left"></i>
          </button>
          
          <div class="testimonials-track">
            <div 
              v-for="(testimonial, index) in testimonials" 
              :key="index"
              class="testimonial-slide"
              :class="{ active: index === currentTestimonialIndex }"
            >
              <div class="testimonial-card">
                <div class="testimonial-stars">
                  <i v-for="n in 5" :key="n" class="pi pi-star-fill"></i>
                </div>
                <p class="testimonial-text">"{{ testimonial.text }}"</p>
                <div class="testimonial-author">
                  <div class="testimonial-avatar">
                    <i class="pi pi-user"></i>
                  </div>
                  <div class="testimonial-info">
                    <div class="testimonial-name">{{ testimonial.name }}</div>
                    <div class="testimonial-role">{{ testimonial.role }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <button @click="nextTestimonial" class="testimonial-btn testimonial-btn-next">
            <i class="pi pi-chevron-right"></i>
          </button>
        </div>
        
        <div class="testimonial-indicators">
          <button 
            v-for="(testimonial, index) in testimonials" 
            :key="index"
            @click="goToTestimonial(index)"
            class="testimonial-indicator"
            :class="{ active: index === currentTestimonialIndex }"
          ></button>
        </div>
        
        <!-- Feedback Modal -->
        <div v-if="showFeedbackModal" class="modal-overlay" @click.self="showFeedbackModal = false">
          <div class="feedback-modal">
            <div class="modal-header">
              <h3>Share Your Experience</h3>
              <button @click="showFeedbackModal = false" class="btn-close">&times;</button>
            </div>
            
            <div class="modal-body">
              <div class="form-group">
                <label>Your Rating *</label>
                <div class="star-rating">
                  <i 
                    v-for="star in 5" 
                    :key="star"
                    @click="feedbackForm.rating = star"
                    class="pi"
                    :class="star <= feedbackForm.rating ? 'pi-star-fill' : 'pi-star'"
                  ></i>
                </div>
              </div>
              
              <div class="form-group">
                <label>Your Position *</label>
                <input v-model="feedbackForm.position" type="text" placeholder="e.g., Plant Manager" required>
              </div>
              
              <div class="form-group">
                <label>Your Plant</label>
                <input v-model="feedbackForm.plant" type="text" placeholder="e.g., Agus 2 (optional)">
              </div>
              
              <div class="form-group">
                <label>Your Testimonial *</label>
                <textarea v-model="feedbackForm.testimonial" rows="4" placeholder="Share your experience with the GenTrack..." required></textarea>
              </div>
            </div>
            
            <div class="modal-footer">
              <button @click="showFeedbackModal = false" class="btn-secondary">Cancel</button>
              <button @click="submitFeedback" class="btn-primary">Submit Feedback</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call-to-Action Banner -->
    <transition name="slide-up">
      <div v-if="showCtaBanner" class="cta-banner">
        <div class="cta-banner-content">
          <div class="cta-banner-text">
            <strong>Ready to streamline your reporting?</strong>
            <span>Contact your administrator for access to GenTrack</span>
          </div>
          <div class="cta-banner-actions">
            <router-link to="/login" class="cta-banner-btn">
              Sign In
            </router-link>
            <button @click="dismissCtaBanner" class="cta-banner-dismiss">
              <i class="pi pi-times"></i>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Video Modal -->
    <transition name="modal">
      <div v-if="showVideoModal" class="video-modal" @click="closeVideoModal">
        <div class="video-modal-content" @click.stop>
          <button @click="closeVideoModal" class="video-modal-close">
            <i class="pi pi-times"></i>
          </button>
          <div class="video-player">
            <!-- YouTube/Vimeo Embed -->
            <iframe 
              v-if="useYouTube && videoUrl"
              :src="videoUrl"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
              class="video-iframe"
            ></iframe>
            
            <!-- Local Video File -->
            <video 
              v-else-if="!useYouTube && videoUrl"
              :src="videoUrl"
              controls
              class="video-element"
            >
              Your browser does not support the video tag.
            </video>
            
            <!-- Placeholder when no video -->
            <div v-else class="video-placeholder">
              <i class="pi pi-video"></i>
              <p>Video Demo Placeholder</p>
              <p class="video-note">Add your video URL in the component data</p>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Footer -->
    <footer class="landing-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-brand">
            <!-- Animated SVG Logo for GenTrack -->
            <div class="gentrack-logo footer-logo-svg">
              <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Background Hexagon -->
                <polygon points="50,5 90,27.5 90,72.5 50,95 10,72.5 10,27.5" fill="none" stroke="#3b82f6" stroke-width="6" class="logo-hex"/>
                
                <!-- Power Lightning Bolt -->
                <path d="M55,20 L35,55 L50,55 L45,80 L65,45 L50,45 Z" fill="#60a5fa" class="logo-bolt"/>
                
                <!-- Data Connection Nodes -->
                <circle cx="35" cy="55" r="4" fill="#fb923c" class="logo-node"/>
                <circle cx="50" cy="55" r="4" fill="#fb923c" class="logo-node"/>
                <circle cx="65" cy="45" r="4" fill="#fb923c" class="logo-node"/>
                <circle cx="50" cy="45" r="4" fill="#fb923c" class="logo-node"/>
              </svg>
            </div>
            <p>Generation and Performance Division</p>
            <p class="footer-tagline">Powering Excellence in Reporting</p>
          </div>
          
          <div class="footer-links">
            <div class="footer-column">
              <h4>Product</h4>
              <router-link to="/features">Features</router-link>
              <router-link to="/documentation">Documentation</router-link>
              <router-link to="/support">Support</router-link>
            </div>
            
            <div class="footer-column">
              <h4>Company</h4>
              <router-link to="/about">About GPD</router-link>
              <router-link to="/contact">Contact Us</router-link>
              <router-link to="/careers">Careers</router-link>
            </div>
            
            <div class="footer-column">
              <h4>Legal</h4>
              <router-link to="/privacy">Privacy Policy</router-link>
              <router-link to="/terms">Terms of Service</router-link>
              <router-link to="/security">Security</router-link>
            </div>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2026 Generation and Performance Division. All rights reserved.</p>
          <p class="developer-credit">Developed by <span class="developer-name">Artchel B. Lapuz</span></p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import ThemeControls from './ThemeControls.vue';

export default {
  name: 'LandingPage',
  components: {
    ThemeControls
  },
  data() {
    return {
      scrollY: 0,
      scrollProgress: 0,
      darkMode: false,
      showCtaBanner: false,
      showVideoModal: false,
      videoUrl: '/videos/demo.mp4.mp4', // Local video file path
      useYouTube: false, // Set to true if using YouTube embed
      videoDuration: '0:00', // Will be loaded from video metadata
      stats: {
        plants: 0,
        capacity: 0,
        uptime: 0
      },
      targetStats: {
        plants: 7,
        capacity: 1025,
        uptime: 99.9
      },
      liveStats: {
        activeUsers: 24,
        reportsProcessed: 15847,
        uptime: 99.9,
        avgResponseTime: 145
      },
      currentPlantIndex: 0,
      carouselInterval: null,
      powerPlants: [
        {
          code: 'AGUS1',
          name: 'Agus 1 Hydroelectric Power Plant',
          location: 'Lanao del Sur',
          capacity: 50,
          units: 2,
          description: 'The first hydroelectric power plant in the Agus River system, providing reliable power generation since its commissioning.'
        },
        {
          code: 'AGUS2',
          name: 'Agus 2 Hydroelectric Power Plant',
          location: 'Lanao del Sur',
          capacity: 180,
          units: 5,
          description: 'One of the largest power plants in the system, featuring advanced turbine technology for optimal power generation.'
        },
        {
          code: 'AGUS4',
          name: 'Agus 4 Hydroelectric Power Plant',
          location: 'Lanao del Norte',
          capacity: 100,
          units: 3,
          description: 'A key contributor to the regional power grid with consistent performance and reliability.'
        },
        {
          code: 'AGUS5',
          name: 'Agus 5 Hydroelectric Power Plant',
          location: 'Lanao del Norte',
          capacity: 52,
          units: 2,
          description: 'Strategically positioned to maximize water flow efficiency and power output.'
        },
        {
          code: 'AGUS6',
          name: 'Agus 6 Hydroelectric Power Plant',
          location: 'Lanao del Norte',
          capacity: 200,
          units: 4,
          description: 'The largest power plant in the Agus system, equipped with state-of-the-art generation equipment.'
        },
        {
          code: 'AGUS7',
          name: 'Agus 7 Hydroelectric Power Plant',
          location: 'Lanao del Norte',
          capacity: 68,
          units: 2,
          description: 'The final power plant in the Agus cascade, ensuring maximum utilization of water resources.'
        },
        {
          code: 'PULANGI4',
          name: 'Pulangi 4 Hydroelectric Power Plant',
          location: 'Bukidnon',
          capacity: 255,
          units: 4,
          description: 'A major power generation facility in Mindanao, harnessing the Pulangi River for sustainable energy.'
        }
      ],
      currentTestimonialIndex: 0,
      testimonialInterval: null,
      testimonials: [],
      timeline: [
        {
          date: 'Q1 2025',
          title: 'Project Inception',
          description: 'Initial planning and requirements gathering for the GenTrack',
          details: [
            'Stakeholder consultations with GPD personnel',
            'Requirements analysis and system design',
            'Technology stack selection',
            'Project timeline and milestone planning'
          ],
          impact: 'Established a clear vision and roadmap for modernizing power plant reporting processes across all Agus-Pulangi facilities.'
        },
        {
          date: 'Q2 2025',
          title: 'Development Phase',
          description: 'Core features implemented including dashboard, upload, and reporting modules',
          details: [
            'Real-time dashboard with live data visualization',
            'Excel upload functionality with validation',
            'User authentication and role-based access',
            'Database design and API development'
          ],
          impact: 'Created the foundation of the system with essential features that enable efficient data management and reporting.'
        },
        {
          date: 'Q3 2025',
          title: 'Beta Testing',
          description: 'Pilot deployment across 3 power plants with user feedback integration',
          details: [
            'Deployed to Agus 2, Agus 6, and Pulangi 4',
            'Collected user feedback and identified improvements',
            'Performance optimization and bug fixes',
            'Training sessions for plant operators'
          ],
          impact: 'Validated system functionality in real-world conditions and refined features based on actual user needs.'
        },
        {
          date: 'Q4 2025',
          title: 'Full Launch',
          description: 'System deployed to all 7 Agus-Pulangi power plants',
          details: [
            'Complete rollout to all power plants',
            'Comprehensive user training program',
            'Data migration from legacy systems',
            'Established 24/7 support system'
          ],
          impact: 'Achieved full operational status across the entire Agus-Pulangi system, streamlining reporting for all facilities.'
        },
        {
          date: 'Q1 2026',
          title: 'Enhanced Analytics',
          description: 'Advanced charting and comparison features added based on user requests',
          details: [
            'Interactive charts and trend analysis',
            'Multi-plant comparison tools',
            'Automated report generation',
            'Export functionality in multiple formats'
          ],
          impact: 'Empowered users with powerful analytics tools for better decision-making and performance monitoring.'
        },
        {
          date: 'Q2 2026',
          title: 'Future Roadmap',
          description: 'AI-powered predictive analytics and mobile app in development',
          details: [
            'Machine learning for predictive maintenance',
            'Mobile app for on-the-go access',
            'Advanced forecasting algorithms',
            'Integration with external data sources'
          ],
          impact: 'Positioning the system at the forefront of power generation management technology with cutting-edge features.'
        }
      ],
      showTimelineModal: false,
      selectedMilestone: {},
      comparisonItems: [
        {
          feature: 'Report Processing Time',
          before: '2-3 hours manually',
          after: '5 minutes automated'
        },
        {
          feature: 'Data Accuracy',
          before: 'Manual entry errors',
          after: '99.9% accuracy with validation'
        },
        {
          feature: 'Real-time Monitoring',
          before: 'Not available',
          after: 'Live dashboard updates'
        },
        {
          feature: 'Historical Analysis',
          before: 'Difficult to access',
          after: 'Instant trend visualization'
        },
        {
          feature: 'Multi-plant Comparison',
          before: 'Manual spreadsheet work',
          after: 'One-click comparison'
        },
        {
          feature: 'Report Generation',
          before: 'Hours of formatting',
          after: 'Automated export'
        }
      ],
      newsletterEmail: '',
      newsletterSuccess: false,
      showFeedbackModal: false,
      feedbackForm: {
        rating: 5,
        position: '',
        plant: '',
        testimonial: ''
      },
      activeFaq: null,
      faqs: [
        {
          question: 'What is the GenTrack?',
          answer: 'The GenTrack is a comprehensive platform designed to streamline the management and reporting of power generation data from the Agus-Pulangi hydroelectric power plants. It provides real-time monitoring, data analytics, and automated report generation for the Generation and Performance Division.'
        },
        {
          question: 'How do I upload daily reports?',
          answer: 'Simply navigate to the Upload Excel page, drag and drop your Excel file, or click to browse. The system automatically validates the data format and imports it into the database. Supported file formats include .xlsx and .xls with a maximum file size of 25MB.'
        },
        {
          question: 'Can I export data for external analysis?',
          answer: 'Yes! The system provides comprehensive export functionality. You can generate reports in Excel format with customizable date ranges and plant selections. All exports include detailed metrics, charts, and summary statistics.'
        },
        {
          question: 'What metrics are tracked in the dashboard?',
          answer: 'The dashboard tracks key performance indicators including total generation (MWh), capacity factor (%), availability (%), forced outage rate (%), and real-time plant status. You can view data for individual plants or compare multiple plants side-by-side.'
        },
        {
          question: 'Is the system accessible on mobile devices?',
          answer: 'Yes, the GenTrack is fully responsive and optimized for mobile devices. You can access all features including dashboard monitoring, report viewing, and data uploads from your smartphone or tablet.'
        },
        {
          question: 'How often is the data updated?',
          answer: 'Data is updated in real-time as reports are uploaded. The dashboard features an auto-refresh option that updates every 30 seconds to ensure you always have the latest information. Historical data is preserved for trend analysis.'
        },
        {
          question: 'Who can access the system?',
          answer: 'The system is designed for GPD personnel and authorized stakeholders. Access is controlled through secure authentication, and different user roles have appropriate permissions for viewing, uploading, and managing data.'
        },
        {
          question: 'What support is available if I encounter issues?',
          answer: 'Comprehensive documentation is available within the system, including user guides and troubleshooting tips. For technical support, you can contact the GPD IT support team through the designated channels provided in your user account.'
        }
      ]
    };
  },
  computed: {
  },
  mounted() {
    // Load testimonials from API
    this.loadTestimonials();
    
    // Hide scrollbar but keep scrolling functionality
    document.body.style.overflowX = 'hidden';
    document.documentElement.style.overflowX = 'hidden';
    document.body.style.msOverflowStyle = 'none';
    document.body.style.scrollbarWidth = 'none';
    document.body.classList.add('hide-scrollbar');
    
    // Add scroll listener for parallax and animations
    window.addEventListener('scroll', this.handleScroll);
    
    // Observe elements for scroll animations
    this.observeElements();
    
    // Animate stats when they come into view
    this.setupStatsObserver();
    
    // Start carousel auto-play
    this.startCarousel();
    
    // Start testimonial carousel
    this.startTestimonialCarousel();
    
    // Show CTA banner after scrolling
    setTimeout(() => {
      window.addEventListener('scroll', this.checkCtaBanner);
    }, 3000);
    
    // Load dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode === 'true') {
      this.darkMode = true;
    }
    
    // Simulate live stats updates
    this.startLiveStatsUpdates();
    
    // Load video duration
    this.loadVideoDuration();
  },
  beforeUnmount() {
    document.body.style.overflowX = '';
    document.documentElement.style.overflowX = '';
    document.body.style.msOverflowStyle = '';
    document.body.style.scrollbarWidth = '';
    document.body.classList.remove('hide-scrollbar');
    window.removeEventListener('scroll', this.handleScroll);
    window.removeEventListener('scroll', this.checkCtaBanner);
    this.stopCarousel();
    this.stopTestimonialCarousel();
    if (this.liveStatsInterval) {
      clearInterval(this.liveStatsInterval);
    }
  },
  methods: {
    generateParticleStyle(index) {
      const size = Math.random() * 6 + 2;
      const left = Math.random() * 100;
      const top = Math.random() * 100;
      const duration = Math.random() * 20 + 10;
      const delay = Math.random() * -20;
      
      return {
        width: `${size}px`,
        height: `${size}px`,
        left: `${left}%`,
        top: `${top}%`,
        animationDuration: `${duration}s`,
        animationDelay: `${delay}s`,
        opacity: Math.random() * 0.5 + 0.2
      };
    },
    async loadTestimonials() {
      try {
        const response = await fetch('http://localhost:8000/api/testimonials/');
        const data = await response.json();
        
        // Handle both paginated and non-paginated responses
        const testimonialsList = Array.isArray(data) ? data : (data.results || []);
        
        this.testimonials = testimonialsList.map(t => ({
          name: t.name,
          role: `${t.position}${t.plant ? ', ' + t.plant : ''}`,
          text: t.testimonial,
          rating: t.rating
        }));
        
        // If no testimonials, use fallback
        if (this.testimonials.length === 0) {
          this.testimonials = [{
            name: 'GPD User',
            role: 'Power Plant Personnel',
            text: 'The GenTrack has transformed how we manage daily reports.',
            rating: 5
          }];
        }
      } catch (error) {
        console.error('Error loading testimonials:', error);
        // Fallback to default testimonial if API fails
        this.testimonials = [{
          name: 'GPD User',
          role: 'Power Plant Personnel',
          text: 'The GenTrack has transformed how we manage daily reports.',
          rating: 5
        }];
      }
    },
    handleScroll() {
      this.scrollY = window.scrollY;
      
      // Calculate scroll progress
      const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      this.scrollProgress = (this.scrollY / windowHeight) * 100;
      
      // Parallax effect for hero
      const hero = document.querySelector('.hero-content');
      if (hero) {
        hero.style.transform = `translateY(${this.scrollY * 0.5}px)`;
        hero.style.opacity = 1 - (this.scrollY / 600);
      }
    },
    
    observeElements() {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
          }
        });
      }, {
        threshold: 0.1
      });
      
      // Observe all animatable elements
      document.querySelectorAll('.feature-card, .step-card, .stat-card').forEach(el => {
        observer.observe(el);
      });
    },
    
    setupStatsObserver() {
      const statsSection = document.querySelector('.stats-section');
      if (!statsSection) return;
      
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.animateStats();
            observer.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.5
      });
      
      observer.observe(statsSection);
    },
    
    animateStats() {
      const duration = 2000;
      const steps = 60;
      const interval = duration / steps;
      
      let currentStep = 0;
      
      const timer = setInterval(() => {
        currentStep++;
        const progress = currentStep / steps;
        
        this.stats.plants = Math.floor(this.targetStats.plants * progress);
        this.stats.capacity = Math.floor(this.targetStats.capacity * progress);
        this.stats.uptime = (this.targetStats.uptime * progress).toFixed(1);
        
        if (currentStep >= steps) {
          this.stats.plants = this.targetStats.plants;
          this.stats.capacity = this.targetStats.capacity;
          this.stats.uptime = this.targetStats.uptime;
          clearInterval(timer);
        }
      }, interval);
    },
    
    // Carousel methods
    startCarousel() {
      this.carouselInterval = setInterval(() => {
        this.nextPlant();
      }, 5000); // Auto-advance every 5 seconds
    },
    
    stopCarousel() {
      if (this.carouselInterval) {
        clearInterval(this.carouselInterval);
        this.carouselInterval = null;
      }
    },
    
    nextPlant() {
      this.currentPlantIndex = (this.currentPlantIndex + 1) % this.powerPlants.length;
    },
    
    prevPlant() {
      this.currentPlantIndex = this.currentPlantIndex === 0 
        ? this.powerPlants.length - 1 
        : this.currentPlantIndex - 1;
    },
    
    goToPlant(index) {
      this.currentPlantIndex = index;
      // Reset auto-play timer
      this.stopCarousel();
      this.startCarousel();
    },
    
    // FAQ methods
    toggleFaq(index) {
      this.activeFaq = this.activeFaq === index ? null : index;
    },
    
    // Testimonial carousel methods
    startTestimonialCarousel() {
      this.testimonialInterval = setInterval(() => {
        this.nextTestimonial();
      }, 6000);
    },
    
    stopTestimonialCarousel() {
      if (this.testimonialInterval) {
        clearInterval(this.testimonialInterval);
        this.testimonialInterval = null;
      }
    },
    
    nextTestimonial() {
      this.currentTestimonialIndex = (this.currentTestimonialIndex + 1) % this.testimonials.length;
    },
    
    prevTestimonial() {
      this.currentTestimonialIndex = this.currentTestimonialIndex === 0 
        ? this.testimonials.length - 1 
        : this.currentTestimonialIndex - 1;
    },
    
    goToTestimonial(index) {
      this.currentTestimonialIndex = index;
      this.stopTestimonialCarousel();
      this.startTestimonialCarousel();
    },
    
    // Video modal methods
    openVideoModal() {
      this.showVideoModal = true;
      document.body.style.overflow = 'hidden';
    },
    
    closeVideoModal() {
      this.showVideoModal = false;
      document.body.style.overflow = '';
    },
    
    // Newsletter methods
    scrollToFeatures() {
      const featuresSection = document.getElementById('features');
      if (featuresSection) {
        featuresSection.scrollIntoView({ behavior: 'smooth' });
      }
    },
    subscribeNewsletter() {
      if (this.newsletterEmail && this.newsletterEmail.includes('@')) {
        this.newsletterSuccess = true;
        this.newsletterEmail = '';
        setTimeout(() => {
          this.newsletterSuccess = false;
        }, 5000);
      }
    },
    
    // CTA Banner methods
    checkCtaBanner() {
      if (window.scrollY > 1000 && !this.showCtaBanner) {
        this.showCtaBanner = true;
      }
    },
    
    dismissCtaBanner() {
      this.showCtaBanner = false;
    },
    
    // Dark mode methods
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
      localStorage.setItem('darkMode', this.darkMode);
    },
    
    // Live stats simulation
    startLiveStatsUpdates() {
      this.liveStatsInterval = setInterval(() => {
        // Simulate small random changes
        this.liveStats.activeUsers = 20 + Math.floor(Math.random() * 10);
        this.liveStats.avgResponseTime = 140 + Math.floor(Math.random() * 20);
      }, 5000);
    },
    
    // Load video duration from video file
    loadVideoDuration() {
      if (!this.videoUrl || this.useYouTube) {
        this.videoDuration = '0:00';
        return;
      }
      
      const video = document.createElement('video');
      video.src = this.videoUrl;
      
      video.addEventListener('loadedmetadata', () => {
        const duration = Math.floor(video.duration);
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        this.videoDuration = `${minutes}:${seconds.toString().padStart(2, '0')}`;
      });
      
      video.addEventListener('error', () => {
        console.error('Error loading video metadata');
        this.videoDuration = '0:00';
      });
    },
    
    // Feedback form methods
    async submitFeedback() {
      // Validate required fields
      if (!this.feedbackForm.rating || !this.feedbackForm.position || !this.feedbackForm.testimonial) {
        alert('Please fill in all required fields (Rating, Position, and Testimonial)');
        return;
      }
      
      try {
        const response = await fetch('http://localhost:8000/api/testimonials/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.feedbackForm.position, // Using position as name for now
            position: this.feedbackForm.position,
            plant: this.feedbackForm.plant || null,
            testimonial: this.feedbackForm.testimonial,
            rating: this.feedbackForm.rating
          })
        });
        
        if (response.ok) {
          alert('Thank you for your feedback! Your testimonial has been submitted and is pending approval.');
          // Reset form
          this.feedbackForm = {
            rating: 5,
            position: '',
            plant: '',
            testimonial: ''
          };
          this.showFeedbackModal = false;
        } else {
          const error = await response.json();
          alert('Error submitting feedback: ' + (error.detail || 'Please try again'));
        }
      } catch (error) {
        console.error('Error submitting feedback:', error);
        alert('Error submitting feedback. Please try again later.');
      }
    },
    
    // Timeline modal methods
    openTimelineModal(milestone) {
      this.selectedMilestone = milestone;
      this.showTimelineModal = true;
      document.body.style.overflow = 'hidden';
    },
    
    closeTimelineModal() {
      this.showTimelineModal = false;
      document.body.style.overflow = '';
    }
  }
};
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: #ffffff;
  position: relative;
  overflow-x: hidden;
  width: 100%;
  max-width: 100vw;
}

/* Animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes shimmer {
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
}

/* Scroll Animation Classes */
.feature-card,
.step-card,
.stat-card {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.feature-card.animate-in,
.step-card.animate-in,
.stat-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger animation delays */
.feature-card:nth-child(1) { transition-delay: 0.1s; }
.feature-card:nth-child(2) { transition-delay: 0.2s; }
.feature-card:nth-child(3) { transition-delay: 0.3s; }
.feature-card:nth-child(4) { transition-delay: 0.4s; }

.step-card:nth-child(1) { transition-delay: 0.1s; }
.step-card:nth-child(3) { transition-delay: 0.2s; }
.step-card:nth-child(5) { transition-delay: 0.3s; }

.stat-card:nth-child(1) { transition-delay: 0.1s; }
.stat-card:nth-child(2) { transition-delay: 0.2s; }
.stat-card:nth-child(3) { transition-delay: 0.3s; }
.stat-card:nth-child(4) { transition-delay: 0.4s; }

/* Hero Section */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 80px 20px;
  position: relative;
  overflow: hidden;
}

/* Hero Section Background */
.mesh-gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(at 0% 0%, #1e3a8a 0%, transparent 50%),
    radial-gradient(at 100% 0%, #1e40af 0%, transparent 50%),
    radial-gradient(at 100% 100%, #1e3a8a 0%, transparent 50%),
    radial-gradient(at 0% 100%, #1e40af 0%, transparent 50%),
    radial-gradient(at 50% 50%, #111827 0%, transparent 50%),
    #0f172a;
  filter: blur(10px);
  z-index: 0;
  animation: meshMove 20s ease-in-out infinite alternate;
}

@keyframes meshMove {
  0% { transform: scale(1); }
  100% { transform: scale(1.1); }
}

.energy-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;
}

.energy-particle {
  position: absolute;
  background: #60a5fa;
  border-radius: 50%;
  filter: blur(2px);
  box-shadow: 0 0 10px #3b82f6, 0 0 20px #2563eb;
  animation: floatParticle linear infinite;
}

@keyframes floatParticle {
  0% { transform: translate(0, 0) scale(1); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translate(100px, -200px) scale(0); opacity: 0; }
}

.grain-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3Base-filter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  opacity: 0.05;
  pointer-events: none;
  z-index: 2;
}

.data-grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(59, 130, 246, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.05) 1px, transparent 1px);
  background-size: 50px 50px;
  z-index: 1;
  mask-image: radial-gradient(circle at center, black, transparent 80%);
}

.accent-orbs {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
}

.accent-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: orbFloat 20s infinite alternate;
}

.accent-orb-1 {
  width: 400px;
  height: 400px;
  background: #3b82f6;
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.accent-orb-2 {
  width: 300px;
  height: 300px;
  background: #fb923c;
  bottom: 10%;
  right: -50px;
  animation-delay: -5s;
}

.accent-orb-3 {
  width: 250px;
  height: 250px;
  background: #60a5fa;
  top: 20%;
  right: 20%;
  animation-delay: -10s;
}

@keyframes orbFloat {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(50px, 30px) scale(1.1); }
}

.ui-mockup-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1000px;
  z-index: 1;
}

.ui-mockup {
  width: 700px;
  height: 450px;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  transform: rotateX(50deg) rotateZ(-45deg) translateY(120px);
  opacity: 0.6;
  animation: floatMockup 15s ease-in-out infinite alternate;
  display: flex;
  flex-direction: column;
}

.mockup-header {
  height: 35px;
  background: rgba(59, 130, 246, 0.15);
  display: flex;
  align-items: center;
  padding: 0 15px;
  gap: 8px;
  border-bottom: 1px solid rgba(59, 130, 246, 0.3);
}

.mockup-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.4);
}

.mockup-body {
  display: flex;
  flex-grow: 1;
}

.mockup-sidebar {
  width: 140px;
  background: rgba(59, 130, 246, 0.1);
  border-right: 1px solid rgba(59, 130, 246, 0.3);
}

.mockup-content {
  flex-grow: 1;
  padding: 25px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.mockup-row {
  height: 25px;
  background: rgba(59, 130, 246, 0.15);
  border-radius: 5px;
}

@keyframes floatMockup {
  0% {
    transform: rotateX(50deg) rotateZ(-45deg) translateY(120px) scale(0.98);
    opacity: 0.5;
  }
  100% {
    transform: rotateX(48deg) rotateZ(-42deg) translateY(100px) scale(1);
    opacity: 0.7;
  }
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    rgba(15, 23, 42, 0.7) 0%,
    rgba(30, 41, 59, 0.5) 100%
  );
  z-index: 3;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
  pointer-events: none;
  animation: pulse 8s ease-in-out infinite;
}

.hero-section::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(59, 130, 246, 0.05) 50%,
    transparent 70%
  );
  animation: shimmer 15s linear infinite;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 4;
}

.hero-content {
  max-width: 900px;
  margin: 0 auto;
  animation: fadeInUp 1s ease-out;
  transition: transform 0.1s ease-out, opacity 0.1s ease-out;
}

/* GenTrack SVG Logo Animations */
.hero-logo-svg {
  width: 120px;
  height: 120px;
  margin: 0 auto;
}

.hero-logo-svg svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 12px rgba(59, 130, 246, 0.6));
}

.footer-logo-svg {
  width: 60px;
  height: 60px;
  margin-bottom: 20px;
}

.footer-logo-svg svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 0 6px rgba(59, 130, 246, 0.4));
}

.logo-hex {
  stroke-dasharray: 260;
  stroke-dashoffset: 0;
  animation: drawHex 4s ease-in-out infinite alternate;
}

.logo-bolt {
  transform-origin: center;
  animation: pulseBolt 2s infinite alternate;
}

.logo-node {
  animation: blinkNode 2s infinite;
}

.logo-node:nth-child(3) { animation-delay: 0s; }
.logo-node:nth-child(4) { animation-delay: 0.5s; }
.logo-node:nth-child(5) { animation-delay: 1s; }
.logo-node:nth-child(6) { animation-delay: 1.5s; }

@keyframes drawHex {
  0% { stroke-dashoffset: 260; }
  50% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: 0; }
}

@keyframes pulseBolt {
  0% { transform: scale(0.95); fill: #3b82f6; }
  100% { transform: scale(1.05); fill: #93c5fd; }
}

@keyframes blinkNode {
  0%, 100% { opacity: 0.3; r: 3; fill: #fb923c; }
  50% { opacity: 1; r: 5; fill: #fde047; }
}

.logo-hero {
  margin-bottom: 30px;
  animation: float 3s ease-in-out infinite;
}

#hero .hero-title {
  font-size: 4rem;
  font-weight: 800;
  color: #ffffff !important;
  margin: 0 0 20px 0;
  letter-spacing: -0.02em;
  text-shadow: none !important;
  animation: fadeInDown 1s ease-out 0.2s both;
}

#hero .hero-subtitle {
  font-size: 1.5rem;
  color: #ffffff !important;
  margin: 0 0 15px 0;
  text-shadow: none !important;
  animation: fadeInDown 1s ease-out 0.4s both;
}

#hero .hero-tagline {
  font-size: 1.125rem;
  color: #ffffff !important;
  margin: 0 0 40px 0;
  line-height: 1.6;
  text-shadow: none !important;
  animation: fadeInDown 1s ease-out 0.6s both;
}

.scroll-hint {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  z-index: 5;
  transition: opacity 0.3s;
  animation: fadeIn 1.5s ease-out 1s both;
}

.scroll-hint:hover {
  opacity: 0.8;
}

.mouse {
  width: 26px;
  height: 42px;
  border: 2px solid #ffffff;
  border-radius: 15px;
  position: relative;
}

.wheel {
  width: 4px;
  height: 8px;
  background: #ffffff;
  border-radius: 2px;
  position: absolute;
  top: 6px;
  left: 50%;
  transform: translateX(-50%);
  animation: scrollWheel 2s infinite;
}

.arrows {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.arrows span {
  display: block;
  width: 10px;
  height: 10px;
  border-bottom: 2px solid #ffffff;
  border-right: 2px solid #ffffff;
  transform: rotate(45deg);
  margin: -5px;
  animation: arrowDown 2s infinite;
}

.arrows span:nth-child(2) { animation-delay: -0.2s; }
.arrows span:nth-child(3) { animation-delay: -0.4s; }

@keyframes scrollWheel {
  0% { transform: translate(-50%, 0); opacity: 1; }
  100% { transform: translate(-50%, 15px); opacity: 0; }
}

@keyframes arrowDown {
  0% { opacity: 0; transform: rotate(45deg) translate(-10px, -10px); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: rotate(45deg) translate(10px, 10px); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 1s ease-out 0.8s both;
}

.btn {
  padding: 16px 40px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn:hover::before {
  width: 300px;
  height: 300px;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
}

.btn-primary:active {
  transform: translateY(-1px);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 255, 255, 0.1);
}

.btn i {
  transition: transform 0.3s ease;
}

.btn:hover i {
  transform: translateX(3px);
}

/* Features Section */
.features-section {
  padding: 100px 20px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: relative;
}

.features-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 50%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  text-align: center;
  margin: 0 0 15px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.section-subtitle {
  font-size: 1.125rem;
  color: #475569;
  text-align: center;
  margin: 0 0 60px 0;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
  margin-top: 60px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 1200px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
}

.feature-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.05) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 50px 35px;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  min-height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s ease;
}

.feature-card:hover::before {
  left: 100%;
}

.feature-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(59, 130, 246, 0.1),
    transparent
  );
  transition: left 0.5s ease;
}

.feature-card:hover::before {
  left: 100%;
}

.feature-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border-color: #3b82f6;
}

.feature-icon {
  width: 90px;
  height: 90px;
  margin: 0 auto 25px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 1) 0%, rgba(139, 92, 246, 1) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.8rem;
  color: white;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4),
              0 4px 12px rgba(139, 92, 246, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.feature-icon::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 70%
  );
  transform: rotate(45deg);
  animation: shimmer 3s linear infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%) translateY(-100%) rotate(45deg);
  }
  100% {
    transform: translateX(100%) translateY(100%) rotate(45deg);
  }
}

.feature-card:hover .feature-icon {
  transform: rotateY(360deg) scale(1.1);
  box-shadow: 0 12px 36px rgba(59, 130, 246, 0.6),
              0 6px 18px rgba(139, 92, 246, 0.5);
  background: linear-gradient(135deg, rgba(37, 99, 235, 1) 0%, rgba(109, 40, 217, 1) 100%);
}

.feature-card h3 {
  font-size: 1.6rem;
  color: #1e293b;
  margin: 0 0 15px 0;
  font-weight: 600;
  transition: color 0.3s ease;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feature-card:hover h3 {
  color: #2563eb;
}

.feature-card p {
  font-size: 1.05rem;
  color: #334155;
  line-height: 1.6;
  margin: 0;
  transition: color 0.3s ease;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.feature-card:hover p {
  color: #475569;
}

/* Stats Section */
.stats-section {
  padding: 80px 20px;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(109, 40, 217, 0.3) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.stats-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
  pointer-events: none;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  position: relative;
  z-index: 1;
}

.stat-card {
  text-align: center;
  padding: 30px 20px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.1) 100%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(59, 130, 246, 0.1) 50%,
    transparent 70%
  );
  transform: rotate(45deg);
  animation: shimmer 4s linear infinite;
}

.stat-card:hover {
  transform: translateY(-10px) scale(1.05);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%);
  border-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.stat-number {
  font-size: 3.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
  transition: transform 0.3s ease;
}

.stat-card:hover .stat-number {
  transform: scale(1.1);
}

.stat-label {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* Plant Showcase Carousel */
.plants-carousel-section {
  padding: 100px 20px;
  background: linear-gradient(180deg, #f8fafc 0%, #ffffff 50%, #f8fafc 100%);
  overflow: hidden;
  position: relative;
}

.plants-carousel-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.05) 0%, transparent 50%),
              radial-gradient(circle at 80% 70%, rgba(139, 92, 246, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

.carousel-container {
  position: relative;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 80px;
  perspective: 1500px;
}

.carousel-track {
  position: relative;
  height: 550px;
  overflow: visible;
}

.carousel-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transform: translateX(100%) scale(0.85) rotateY(15deg);
  transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
  pointer-events: none;
  filter: blur(3px);
}

.carousel-slide.active {
  opacity: 1;
  transform: translateX(0) scale(1) rotateY(0deg);
  pointer-events: auto;
  filter: blur(0);
  z-index: 2;
}

.plant-showcase-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 24px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08),
              0 8px 20px rgba(59, 130, 246, 0.05);
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  transform-style: preserve-3d;
}

.plant-showcase-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.03) 0%, rgba(139, 92, 246, 0.03) 100%);
  opacity: 0;
  transition: opacity 0.5s ease;
  pointer-events: none;
  z-index: 1;
}

.plant-showcase-card:hover::before {
  opacity: 1;
}

.plant-showcase-card:hover {
  transform: translateY(-15px) scale(1.02);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.12),
              0 15px 35px rgba(59, 130, 246, 0.15),
              0 0 0 1px rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.3);
}

.plant-image-placeholder {
  height: 280px;
  background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease;
}

.plant-image-placeholder::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
              radial-gradient(circle at 70% 30%, rgba(139, 92, 246, 0.2) 0%, transparent 40%);
  animation: rotate 20s linear infinite;
  opacity: 0;
  transition: opacity 0.5s ease;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.plant-showcase-card:hover .plant-image-placeholder::before {
  opacity: 1;
}

.plant-image-placeholder::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transition: left 0.7s ease;
}

.plant-showcase-card:hover .plant-image-placeholder::after {
  left: 100%;
}

.plant-image-placeholder i {
  font-size: 6rem;
  color: rgba(255, 255, 255, 0.15);
  z-index: 1;
  animation: float 4s ease-in-out infinite;
  transition: all 0.5s ease;
  filter: drop-shadow(0 10px 20px rgba(0, 0, 0, 0.3));
}

.plant-showcase-card:hover .plant-image-placeholder i {
  color: rgba(255, 255, 255, 0.3);
  transform: scale(1.1) rotate(5deg);
}

.plant-code-overlay {
  position: absolute;
  top: 24px;
  right: 24px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.95) 0%, rgba(37, 99, 235, 0.95) 100%);
  backdrop-filter: blur(20px);
  color: white;
  padding: 10px 20px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1.125rem;
  z-index: 2;
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  letter-spacing: 0.5px;
}

.plant-showcase-card:hover .plant-code-overlay {
  transform: scale(1.1) translateY(-5px);
  box-shadow: 0 12px 35px rgba(59, 130, 246, 0.5),
              0 0 0 1px rgba(255, 255, 255, 0.2) inset;
}

.plant-showcase-content {
  padding: 35px;
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 2;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
  backdrop-filter: blur(10px);
}

.plant-showcase-content h3 {
  font-size: 1.875rem;
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 24px 0;
  font-weight: 800;
  letter-spacing: -0.5px;
  transition: all 0.3s ease;
}

.plant-showcase-card:hover .plant-showcase-content h3 {
  transform: translateX(5px);
}

.plant-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.plant-detail-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #475569;
  font-size: 1rem;
  font-weight: 500;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.plant-showcase-card:hover .plant-detail-item {
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  border-color: #bfdbfe;
  transform: translateY(-2px);
}

.plant-detail-item i {
  color: #3b82f6;
  font-size: 1.25rem;
  transition: all 0.3s ease;
}

.plant-showcase-card:hover .plant-detail-item i {
  transform: scale(1.2) rotate(5deg);
}

.plant-description {
  color: #64748b;
  line-height: 1.8;
  margin: 0;
  flex: 1;
  font-size: 1.0625rem;
  transition: all 0.3s ease;
}

.plant-showcase-card:hover .plant-description {
  color: #475569;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border: 2px solid #e2e8f0;
  color: #3b82f6;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08),
              0 4px 10px rgba(59, 130, 246, 0.1);
  backdrop-filter: blur(10px);
}

.carousel-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.carousel-btn:hover::before {
  opacity: 1;
}

.carousel-btn:hover {
  color: white;
  border-color: #3b82f6;
  transform: translateY(-50%) scale(1.15);
  box-shadow: 0 12px 35px rgba(59, 130, 246, 0.3),
              0 6px 15px rgba(59, 130, 246, 0.2);
}

.carousel-btn:active {
  transform: translateY(-50%) scale(1.05);
}

.carousel-btn-prev {
  left: 0;
}

.carousel-btn-next {
  right: 0;
}

.carousel-indicators {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 40px;
}

.carousel-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #cbd5e1;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  padding: 0;
  position: relative;
}

.carousel-indicator::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #3b82f6;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.carousel-indicator:hover {
  background: #94a3b8;
  transform: scale(1.3);
}

.carousel-indicator.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  width: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.carousel-indicator.active::before {
  opacity: 0;
}

/* FAQ Section */
.faq-section {
  padding: 100px 20px;
  background: #f8fafc;
}

.faq-grid {
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.faq-item {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.faq-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
}

.faq-item.active {
  border-color: #3b82f6;
  box-shadow: 0 8px 30px rgba(59, 130, 246, 0.15);
}

.faq-question {
  padding: 25px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.faq-item:hover .faq-question {
  background: #f8fafc;
}

.faq-item.active .faq-question {
  background: #eff6ff;
}

.faq-question h3 {
  font-size: 1.125rem;
  color: #1e293b;
  margin: 0;
  font-weight: 600;
  flex: 1;
}

.faq-question i {
  color: #3b82f6;
  font-size: 1.25rem;
  transition: transform 0.3s ease;
}

.faq-item.active .faq-question i {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 30px 25px 30px;
}

.faq-answer p {
  color: #64748b;
  line-height: 1.8;
  margin: 0;
  font-size: 1rem;
}

/* FAQ Answer Transition */
.faq-answer-enter-active,
.faq-answer-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
}

.faq-answer-enter-from,
.faq-answer-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}

/* How It Works Section */
.how-it-works-section {
  padding: 100px 20px;
  background: #f8fafc;
}

.steps-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  gap: 30px;
  align-items: center;
  margin-top: 60px;
}

.step-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 40px 30px;
  text-align: center;
  position: relative;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.step-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border-color: #3b82f6;
}

.step-number {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
  transition: all 0.3s ease;
}

.step-card:hover .step-number {
  transform: translateX(-50%) scale(1.2) rotate(360deg);
}

.step-icon {
  width: 70px;
  height: 70px;
  margin: 20px auto 20px;
  background: #eff6ff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: #3b82f6;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.step-card:hover .step-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  transform: scale(1.1) rotate(5deg);
}

.step-card h3 {
  font-size: 1.375rem;
  color: #1e293b;
  margin: 0 0 15px 0;
  font-weight: 600;
  transition: color 0.3s ease;
}

.step-card:hover h3 {
  color: #3b82f6;
}

.step-card p {
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.step-arrow {
  font-size: 2rem;
  color: #cbd5e0;
  transition: all 0.3s ease;
  animation: pulse 2s ease-in-out infinite;
}

.step-arrow:hover {
  color: #3b82f6;
  transform: scale(1.2);
}

/* Footer */
.landing-footer {
  background: #1e293b;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 60px 20px 30px;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: 60px;
  margin-bottom: 40px;
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-brand p {
  color: white;
  font-size: 1.125rem;
  font-weight: 600;
  margin: 0;
}

.footer-tagline {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9375rem !important;
  font-weight: 400 !important;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
}

.footer-column h4 {
  color: white;
  font-size: 1rem;
  margin: 0 0 20px 0;
  font-weight: 600;
}

.footer-column a {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  margin-bottom: 12px;
  transition: all 0.3s ease;
  font-size: 0.9375rem;
  position: relative;
  padding-left: 0;
}

.footer-column a::before {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 0;
  height: 2px;
  background: #3b82f6;
  transition: width 0.3s ease;
}

.footer-column a:hover {
  color: #3b82f6;
  padding-left: 10px;
}

.footer-column a:hover::before {
  width: 20px;
}

.footer-bottom {
  text-align: center;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.footer-bottom p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
  margin: 0;
  margin-bottom: 8px;
}

.developer-credit {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.4);
}

.developer-name {
  color: #10b981;
  font-weight: 600;
  transition: color 0.3s ease;
}

.developer-name:hover {
  color: #059669;
}

/* Scroll Progress Bar */
.scroll-progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
  z-index: 9999;
  transition: width 0.1s ease-out;
  box-shadow: 0 2px 10px rgba(59, 130, 246, 0.5);
}

/* Dark Mode Styles */
.landing-page.dark-mode {
  background: #0f172a;
}

.dark-mode .features-section,
.dark-mode .faq-section,
.dark-mode .how-it-works-section,
.dark-mode .comparison-section {
  background: #1e293b;
}

/* Hero Section Dark Mode */
.dark-mode .hero-section {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

.dark-mode .hero-title {
  color: white;
}

.dark-mode .hero-subtitle,
.dark-mode .hero-tagline {
  color: #cbd5e1;
}

/* Section Titles and Subtitles */
.dark-mode .section-title {
  color: white;
}

.dark-mode .section-subtitle {
  color: #94a3b8;
}

/* Feature Cards */
.dark-mode .feature-card,
.dark-mode .step-card,
.dark-mode .faq-item,
.dark-mode .plant-showcase-card,
.dark-mode .testimonial-card {
  background: #334155;
  border-color: #475569;
  color: white;
}

.dark-mode .feature-card h3,
.dark-mode .step-card h3,
.dark-mode .faq-question h3,
.dark-mode .plant-showcase-content h3 {
  color: white;
}

.dark-mode .feature-card p,
.dark-mode .step-card p,
.dark-mode .faq-answer p,
.dark-mode .plant-description,
.dark-mode .plant-detail-item {
  color: #cbd5e1;
}

/* Stats Section Dark Mode */
.dark-mode .stats-section {
  background: #1e293b;
}

.dark-mode .stat-number {
  color: white;
}

.dark-mode .stat-label {
  color: #94a3b8;
}

/* Plant Carousel Dark Mode */
.dark-mode .plants-carousel-section {
  background: #0f172a;
}

.dark-mode .plant-code-overlay {
  color: white;
}

.dark-mode .plant-showcase-card {
  background: #334155;
  border-color: #475569;
}

.dark-mode .plant-showcase-content {
  background: linear-gradient(180deg, rgba(51, 65, 85, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
}

.dark-mode .plant-showcase-content h3 {
  background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.dark-mode .plant-detail-item {
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
  border-color: #475569;
  color: #cbd5e1;
}

.dark-mode .plant-showcase-card:hover .plant-detail-item {
  background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
  border-color: #3b82f6;
}

.dark-mode .plant-detail-item span {
  color: #cbd5e1;
}

.dark-mode .plant-detail-item i {
  color: #60a5fa;
}

.dark-mode .plant-description {
  color: #94a3b8;
}

.dark-mode .carousel-btn {
  background: #334155;
  border-color: #475569;
  color: #3b82f6;
}

.dark-mode .carousel-btn:hover {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.dark-mode .carousel-indicator {
  background: #475569;
}

.dark-mode .carousel-indicator:hover {
  background: #64748b;
}

.dark-mode .carousel-indicator.active {
  background: #3b82f6;
}

/* Live Stats Dark Mode */
.dark-mode .live-stats-section {
  background: #1e293b;
}

.dark-mode .live-stat-card {
  background: #334155;
  border-color: #475569;
}

.dark-mode .live-stat-value {
  color: white;
}

.dark-mode .live-stat-label {
  color: #94a3b8;
}

/* Testimonials Dark Mode */
.dark-mode .testimonials-section {
  background: #0f172a;
}

.dark-mode .testimonial-text {
  color: #cbd5e1;
}

.dark-mode .testimonial-name {
  color: white;
}

.dark-mode .testimonial-role {
  color: #94a3b8;
}

/* Video Demo Dark Mode */
.dark-mode .video-demo-section {
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 50%, #1e293b 100%);
}

/* Timeline Dark Mode */
.dark-mode .timeline-section {
  background: #0f172a;
}

.dark-mode .timeline-content {
  background: #334155;
  border-color: #475569;
}

.dark-mode .timeline-content h3 {
  color: white;
}

.dark-mode .timeline-content p {
  color: #cbd5e1;
}

/* Comparison Table Dark Mode */
.dark-mode .comparison-section {
  background: #1e293b;
}

.dark-mode .comparison-table {
  background: #334155;
  border-color: #475569;
}

.dark-mode .comparison-feature {
  color: white;
}

.dark-mode .comparison-row {
  border-bottom-color: #475569;
}

.dark-mode .comparison-row:hover {
  background: #3f4f63;
}

.dark-mode .comparison-value.before {
  background: rgba(239, 68, 68, 0.1);
  color: #fca5a5;
}

.dark-mode .comparison-value.after {
  background: rgba(16, 185, 129, 0.1);
  color: #6ee7b7;
}

/* FAQ Dark Mode */
.dark-mode .faq-section {
  background: #0f172a;
}

.dark-mode .faq-item {
  background: #1e293b;
  border-color: #475569;
}

.dark-mode .faq-item:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2);
}

.dark-mode .faq-item.active {
  border-color: #3b82f6;
  box-shadow: 0 8px 30px rgba(59, 130, 246, 0.25);
}

.dark-mode .faq-item:hover .faq-question {
  background: #334155;
}

.dark-mode .faq-item.active .faq-question {
  background: rgba(59, 130, 246, 0.1);
}

.dark-mode .faq-question h3 {
  color: white;
}

.dark-mode .faq-question i {
  color: #60a5fa;
}

.dark-mode .faq-answer {
  background: #1e293b;
}

.dark-mode .faq-answer p {
  color: #cbd5e1;
}

/* How It Works Dark Mode */
.dark-mode .how-it-works-section {
  background: #0f172a;
}

.dark-mode .step-number {
  color: white;
}

/* Footer Dark Mode */
.dark-mode .landing-footer {
  background: #0f172a;
  border-top-color: #334155;
}

.dark-mode .footer-brand p {
  color: #cbd5e1;
}

.dark-mode .footer-tagline {
  color: #94a3b8;
}

.dark-mode .footer-column h4 {
  color: white;
}

.dark-mode .footer-column a {
  color: #94a3b8;
}

.dark-mode .footer-column a:hover {
  color: white;
}

.dark-mode .footer-bottom p {
  color: #64748b;
}

/* Live Stats Dashboard */
.live-stats-section {
  padding: 100px 20px;
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: relative;
}

.live-stats-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 60%),
              radial-gradient(circle at 70% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 60%);
  pointer-events: none;
}

.live-stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 35px;
  margin-top: 60px;
  max-width: 1400px;
  margin-left: auto;
  margin-right: auto;
}

@media (max-width: 1200px) {
  .live-stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .live-stats-grid {
    grid-template-columns: 1fr;
  }
}

.live-stat-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.3) 0%, rgba(255, 255, 255, 0.2) 100%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 16px;
  padding: 35px 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: all 0.4s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  min-height: 200px;
  justify-content: center;
}

.live-stat-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(139, 92, 246, 0.15) 50%,
    transparent 70%
  );
  transform: rotate(45deg);
  animation: shimmer 5s linear infinite;
}

.live-stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, rgba(59, 130, 246, 0.8) 0%, rgba(139, 92, 246, 0.8) 100%);
  transform: scaleY(0);
  transition: transform 0.4s ease;
}

.live-stat-card:hover::before {
  transform: scaleY(1);
}

.live-stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.35) 0%, rgba(255, 255, 255, 0.25) 100%);
}

.live-stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.9) 0%, rgba(139, 92, 246, 0.9) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  flex-shrink: 0;
  transition: all 0.4s ease;
  margin-bottom: 20px;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4),
              0 4px 12px rgba(139, 92, 246, 0.3);
}

.live-stat-card:hover .live-stat-icon {
  background: linear-gradient(135deg, rgba(37, 99, 235, 1) 0%, rgba(109, 40, 217, 1) 100%);
  color: white;
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 12px 36px rgba(59, 130, 246, 0.6),
              0 6px 18px rgba(139, 92, 246, 0.5);
}

.live-stat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.live-stat-value {
  font-size: 2.75rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
  margin-bottom: 10px;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.5);
}

.live-stat-label {
  font-size: 1rem;
  color: #1e293b;
  margin-bottom: 12px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
}

.live-stat-trend {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.875rem;
  font-weight: 600;
}

.live-stat-trend.positive {
  color: #059669;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
  font-weight: 700;
}

.live-stat-trend i {
  font-size: 0.75rem;
}

/* Testimonials Section */
.testimonials-section {
  padding: 100px 20px;
  background: #f8fafc;
}

.testimonials-carousel {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 60px;
}

.testimonials-track {
  position: relative;
  height: 350px;
  overflow: hidden;
}

.testimonial-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transform: translateX(100%) scale(0.9);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
}

.testimonial-slide.active {
  opacity: 1;
  transform: translateX(0) scale(1);
  pointer-events: auto;
}

.testimonial-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.testimonial-stars {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-bottom: 25px;
  font-size: 1.25rem;
  color: #fbbf24;
}

.testimonial-text {
  font-size: 1.125rem;
  color: #475569;
  line-height: 1.8;
  margin: 0 0 30px 0;
  font-style: italic;
  flex: 1;
}

.testimonial-author {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.testimonial-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.testimonial-info {
  text-align: left;
}

.testimonial-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 5px;
}

.testimonial-role {
  font-size: 0.9375rem;
  color: #64748b;
}

.testimonial-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: white;
  border: 2px solid #e2e8f0;
  color: #3b82f6;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.testimonial-btn:hover {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.testimonial-btn-prev {
  left: 0;
}

.testimonial-btn-next {
  right: 0;
}

.testimonial-indicators {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 30px;
}

.testimonial-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #cbd5e1;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.testimonial-indicator:hover {
  background: #94a3b8;
  transform: scale(1.2);
}

.testimonial-indicator.active {
  background: #3b82f6;
  width: 32px;
  border-radius: 6px;
}

/* Feedback CTA and Modal */
.feedback-cta {
  text-align: center;
  margin-bottom: 40px;
}

.btn-feedback {
  padding: 14px 32px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.btn-feedback:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.feedback-modal {
  background: white;
  border-radius: 16px;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: fadeInUp 0.3s ease-out;
}

.modal-header {
  padding: 24px 30px;
  border-bottom: 2px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #1e293b;
  font-weight: 700;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #64748b;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.3s ease;
  line-height: 1;
  padding: 0;
}

.btn-close:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.modal-body {
  padding: 30px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.star-rating {
  display: flex;
  gap: 8px;
  font-size: 2rem;
}

.star-rating i {
  cursor: pointer;
  transition: all 0.2s ease;
  color: #fbbf24 !important;
}

.star-rating i.pi-star-fill {
  color: #fbbf24 !important;
  text-shadow: 0 2px 4px rgba(251, 191, 36, 0.4);
}

.star-rating i.pi-star {
  color: #d1d5db !important;
}

.star-rating i:hover {
  transform: scale(1.2);
  filter: brightness(1.2);
}

.modal-footer {
  padding: 20px 30px;
  border-top: 2px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-footer .btn-secondary {
  padding: 12px 24px;
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-footer .btn-secondary:hover {
  background: #e2e8f0;
}

.modal-footer .btn-primary {
  padding: 12px 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
}

.modal-footer .btn-primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

/* Video Demo Section */
.video-demo-section {
  padding: 120px 20px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.video-demo-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
  pointer-events: none;
}

.video-container {
  max-width: 1100px;
  margin: 0 auto;
  cursor: pointer;
  position: relative;
  perspective: 1500px;
}

.video-thumbnail {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.8) 0%, rgba(30, 41, 59, 0.8) 50%, rgba(51, 65, 85, 0.8) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.2),
              0 10px 30px rgba(59, 130, 246, 0.15),
              0 0 0 1px rgba(255, 255, 255, 0.15) inset;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  transform-style: preserve-3d;
}

.video-thumbnail::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at center, rgba(59, 130, 246, 0.15) 0%, transparent 70%),
              radial-gradient(circle at 70% 30%, rgba(139, 92, 246, 0.1) 0%, transparent 50%);
  opacity: 0;
  transition: opacity 0.6s ease;
  animation: pulse 4s ease-in-out infinite;
}

.video-thumbnail:hover::before {
  opacity: 1;
}

.video-thumbnail::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 30%,
    rgba(255, 255, 255, 0.03) 50%,
    transparent 70%
  );
  animation: shimmer 3s linear infinite;
  opacity: 0;
  transition: opacity 0.6s ease;
}

.video-thumbnail:hover::after {
  opacity: 1;
}

.video-thumbnail:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 35px 90px rgba(0, 0, 0, 0.2),
              0 15px 40px rgba(59, 130, 246, 0.2),
              0 0 0 1px rgba(59, 130, 246, 0.2) inset;
}

.video-play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.85) 0%, rgba(37, 99, 235, 0.85) 100%);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 15px 50px rgba(59, 130, 246, 0.4),
              0 0 0 0 rgba(59, 130, 246, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  animation: playPulse 2s ease-in-out infinite;
  z-index: 2;
}

@keyframes playPulse {
  0%, 100% {
    box-shadow: 0 15px 50px rgba(59, 130, 246, 0.4),
                0 0 0 0 rgba(59, 130, 246, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.2) inset;
  }
  50% {
    box-shadow: 0 15px 50px rgba(59, 130, 246, 0.6),
                0 0 0 20px rgba(59, 130, 246, 0),
                0 0 0 1px rgba(255, 255, 255, 0.3) inset;
  }
}

.video-thumbnail:hover .video-play-button {
  transform: translate(-50%, -50%) scale(1.15);
  background: linear-gradient(135deg, rgba(37, 99, 235, 1) 0%, rgba(29, 78, 216, 1) 100%);
  box-shadow: 0 20px 60px rgba(59, 130, 246, 0.6),
              0 0 0 0 rgba(59, 130, 246, 0),
              0 0 0 1px rgba(255, 255, 255, 0.3) inset;
  animation: none;
}

.video-play-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 140px;
  height: 140px;
  border-radius: 50%;
  border: 2px solid rgba(59, 130, 246, 0.3);
  animation: ripple 2s ease-out infinite;
}

@keyframes ripple {
  0% {
    width: 120px;
    height: 120px;
    opacity: 1;
  }
  100% {
    width: 180px;
    height: 180px;
    opacity: 0;
  }
}

.video-play-button i {
  margin-left: 10px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  transition: transform 0.3s ease;
}

.video-thumbnail:hover .video-play-button i {
  transform: scale(1.1);
}

.video-overlay {
  position: absolute;
  bottom: 24px;
  right: 24px;
  z-index: 3;
}

.video-duration {
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
  backdrop-filter: blur(20px);
  color: white;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3),
              0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.video-thumbnail:hover .video-duration {
  transform: translateY(-5px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4),
              0 0 0 1px rgba(255, 255, 255, 0.2) inset;
}

/* Video Modal */
.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.video-modal-content {
  position: relative;
  width: 100%;
  max-width: 1200px;
  background: #1e293b;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
}

.video-modal-close {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1.25rem;
  cursor: pointer;
  z-index: 10;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-modal-close:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1) rotate(90deg);
}

.video-player {
  width: 100%;
  padding-bottom: 56.25%;
  position: relative;
}

.video-iframe,
.video-element {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.video-element {
  background: #000;
}

.video-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.6);
  gap: 15px;
}

.video-placeholder i {
  font-size: 4rem;
}

.video-placeholder p {
  margin: 0;
  font-size: 1.125rem;
}

.video-note {
  font-size: 0.875rem !important;
  color: rgba(255, 255, 255, 0.4) !important;
}

/* Timeline Modal */
.timeline-modal {
  background: white;
  border-radius: 16px;
  max-width: 700px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: fadeInUp 0.3s ease-out;
}

.timeline-modal-date {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  color: #3b82f6;
  padding: 10px 20px;
  border-radius: 20px;
  font-size: 0.9375rem;
  font-weight: 600;
  margin-bottom: 24px;
}

.timeline-modal-date i {
  font-size: 1rem;
}

.timeline-modal-description h4,
.timeline-modal-details h4,
.timeline-modal-impact h4 {
  font-size: 1.125rem;
  color: #1e293b;
  margin: 0 0 16px 0;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}

.timeline-modal-description h4::before {
  content: '📋';
  font-size: 1.25rem;
}

.timeline-modal-details h4::before {
  content: '✨';
  font-size: 1.25rem;
}

.timeline-modal-impact h4::before {
  content: '🎯';
  font-size: 1.25rem;
}

.timeline-modal-description,
.timeline-modal-details,
.timeline-modal-impact {
  margin-bottom: 24px;
}

.timeline-modal-description p,
.timeline-modal-impact p {
  color: #64748b;
  line-height: 1.8;
  margin: 0;
}

.timeline-modal-details ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.timeline-modal-details li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 10px;
  color: #475569;
  line-height: 1.6;
  transition: all 0.3s ease;
}

.timeline-modal-details li:hover {
  background: #eff6ff;
  transform: translateX(5px);
}

.timeline-modal-details li i {
  color: #10b981;
  font-size: 1.125rem;
  margin-top: 2px;
  flex-shrink: 0;
}

/* Dark Mode for Timeline Modal */
.dark-mode .timeline-modal {
  background: #1e293b;
}

.dark-mode .timeline-modal-date {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
  color: #60a5fa;
}

.dark-mode .timeline-modal-description h4,
.dark-mode .timeline-modal-details h4,
.dark-mode .timeline-modal-impact h4 {
  color: white;
}

.dark-mode .timeline-modal-description p,
.dark-mode .timeline-modal-impact p {
  color: #cbd5e1;
}

.dark-mode .timeline-modal-details li {
  background: #0f172a;
  color: #cbd5e1;
}

.dark-mode .timeline-modal-details li:hover {
  background: rgba(59, 130, 246, 0.1);
}

.dark-mode .timeline-content {
  background: #1e293b;
  border-color: #475569;
}

.dark-mode .timeline-content:hover {
  border-color: #3b82f6;
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
}

.dark-mode .timeline-date {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.dark-mode .timeline-content h3 {
  color: white;
}

.dark-mode .timeline-content p {
  color: #cbd5e1;
}

.dark-mode .timeline-click-hint {
  color: #60a5fa;
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .video-modal-content,
.modal-leave-active .video-modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from .video-modal-content,
.modal-leave-to .video-modal-content {
  transform: scale(0.9);
}

/* Timeline Section */
.timeline-section {
  padding: 100px 20px;
  background: #f8fafc;
}

.timeline {
  max-width: 1000px;
  margin: 60px auto 0;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #3b82f6 0%, #8b5cf6 100%);
  transform: translateX(-50%);
}

.timeline-item {
  position: relative;
  margin-bottom: 60px;
  display: flex;
  align-items: center;
}

.timeline-item.left {
  justify-content: flex-end;
  padding-right: calc(50% + 40px);
}

.timeline-item.right {
  justify-content: flex-start;
  padding-left: calc(50% + 40px);
}

.timeline-content {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 25px 30px;
  max-width: 400px;
  transition: all 0.4s ease;
  cursor: pointer;
  position: relative;
}

.timeline-content:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
}

.timeline-click-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8125rem;
  color: #3b82f6;
  margin-top: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
  font-weight: 500;
}

.timeline-content:hover .timeline-click-hint {
  opacity: 1;
}

.timeline-click-hint i {
  font-size: 0.875rem;
}

.timeline-date {
  display: inline-block;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 15px;
}

.timeline-content h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin: 0 0 10px 0;
  font-weight: 700;
}

.timeline-content p {
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
}

.timeline-dot {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: white;
  border: 4px solid #3b82f6;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
  transition: all 0.3s ease;
}

.timeline-item:hover .timeline-dot {
  transform: translateX(-50%) scale(1.5);
  box-shadow: 0 0 0 8px rgba(59, 130, 246, 0.3);
}

/* Comparison Section */
.comparison-section {
  padding: 100px 20px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.comparison-table {
  max-width: 900px;
  margin: 60px auto 0;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
}

.comparison-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: white;
  font-weight: 700;
  font-size: 1.125rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.comparison-col {
  padding: 20px 25px;
  text-align: center;
}

.comparison-col:first-child {
  text-align: left;
}

.comparison-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
}

.comparison-row:last-child {
  border-bottom: none;
}

.comparison-row:hover {
  background: rgba(255, 255, 255, 0.15);
}

.comparison-feature {
  padding: 20px 25px;
  font-weight: 600;
  color: #0f172a;
  display: flex;
  align-items: center;
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
}

.comparison-value {
  padding: 20px 25px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 0.9375rem;
  font-weight: 600;
}

.comparison-value.before {
  color: #dc2626;
  background: rgba(254, 242, 242, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
}

.comparison-value.after {
  color: #059669;
  background: rgba(240, 253, 244, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
}

.comparison-value i {
  font-size: 1.125rem;
}

/* Newsletter Section */
.newsletter-section {
  padding: 80px 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
}

.newsletter-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.newsletter-text h2 {
  font-size: 2.5rem;
  color: white;
  margin: 0 0 15px 0;
  font-weight: 700;
}

.newsletter-text p {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 40px 0;
}

.newsletter-form {
  display: flex;
  gap: 15px;
  max-width: 600px;
  margin: 0 auto;
}

.newsletter-input {
  flex: 1;
  padding: 16px 24px;
  border-radius: 12px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.newsletter-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.newsletter-input:focus {
  outline: none;
  border-color: white;
  background: rgba(255, 255, 255, 0.2);
}

.newsletter-btn {
  padding: 16px 32px;
  border-radius: 12px;
  background: white;
  color: #3b82f6;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.newsletter-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.newsletter-success {
  margin-top: 20px;
  padding: 16px 24px;
  background: rgba(16, 185, 129, 0.2);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(16, 185, 129, 0.5);
  border-radius: 12px;
  color: white;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.newsletter-success i {
  font-size: 1.25rem;
}

/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* CTA Banner */
.cta-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  border-top: 3px solid #3b82f6;
  padding: 20px;
  z-index: 999;
  box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.3);
}

.cta-banner-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.cta-banner-text {
  display: flex;
  align-items: center;
  gap: 15px;
  color: white;
  flex: 1;
}

.cta-banner-text strong {
  font-size: 1.125rem;
  font-weight: 700;
}

.cta-banner-text span {
  color: rgba(255, 255, 255, 0.8);
}

.cta-banner-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.cta-banner-btn {
  padding: 12px 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.cta-banner-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
}

.cta-banner-dismiss {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cta-banner-dismiss:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

/* Slide Up Transition */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.4s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .steps-grid {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  
  .step-arrow {
    transform: rotate(90deg);
  }
  
  .carousel-container {
    padding: 0 50px;
  }
  
  .carousel-btn {
    width: 45px;
    height: 45px;
  }
  
  .timeline::before {
    left: 30px;
  }
  
  .timeline-item.left,
  .timeline-item.right {
    justify-content: flex-start;
    padding-left: 70px;
    padding-right: 0;
  }
  
  .timeline-dot {
    left: 30px;
  }
  
  .comparison-header,
  .comparison-row {
    grid-template-columns: 1.5fr 1fr 1fr;
  }
  
  .cta-banner-content {
    flex-direction: column;
    text-align: center;
  }
  
  .cta-banner-text {
    flex-direction: column;
    gap: 10px;
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.25rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 40px;
  }
  
  .footer-links {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .cta-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }

  .sidebar {
    width: 260px;
    left: -260px;
  }
  
  .carousel-container {
    padding: 0 40px;
  }
  
  .carousel-track {
    height: 550px;
  }
  
  .plant-showcase-content h3 {
    font-size: 1.5rem;
  }
  
  .faq-question {
    padding: 20px;
  }
  
  .faq-answer {
    padding: 0 20px 20px 20px;
  }
  
  .live-stats-grid {
    grid-template-columns: 1fr;
  }
  
  .testimonials-carousel {
    padding: 0 50px;
  }
  
  .testimonials-track {
    height: 400px;
  }
  
  .newsletter-form {
    flex-direction: column;
  }
  
  .newsletter-btn {
    justify-content: center;
  }
  
  .comparison-header,
  .comparison-row {
    grid-template-columns: 1fr;
  }
  
  .comparison-col,
  .comparison-feature,
  .comparison-value {
    text-align: left;
    justify-content: flex-start;
  }
  
  .comparison-header .comparison-col:first-child {
    display: none;
  }
  
  .comparison-feature::before {
    content: attr(data-label);
    font-weight: 700;
    display: block;
    margin-bottom: 5px;
  }
}

@media (max-width: 480px) {
  .hero-logo {
    width: 120px;
    height: 120px;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .carousel-container {
    padding: 0 30px;
  }
  
  .carousel-btn {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .carousel-track {
    height: 600px;
  }
  
  .plant-image-placeholder {
    height: 200px;
  }
  
  .plant-showcase-content {
    padding: 20px;
  }
  
  .plant-showcase-content h3 {
    font-size: 1.25rem;
  }
  
  .faq-question h3 {
    font-size: 1rem;
  }
  
  .testimonials-carousel {
    padding: 0 40px;
  }
  
  .testimonial-btn {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .testimonials-track {
    height: 450px;
  }
  
  .testimonial-card {
    padding: 30px 20px;
  }
  
  .newsletter-text h2 {
    font-size: 2rem;
  }
  
  .timeline-content {
    max-width: 100%;
  }
  
  .cta-banner-text {
    font-size: 0.875rem;
  }
  
  .cta-banner-text strong {
    font-size: 1rem;
  }
}

/* Hide scrollbar for Chrome, Safari and Opera */
::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
body.hide-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

body.hide-scrollbar::-webkit-scrollbar {
  display: none;  /* Chrome, Safari, Opera */
}
</style>
