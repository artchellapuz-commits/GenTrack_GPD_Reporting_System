<template>
  <div class="landing-page" :class="{ 'dark-mode': darkMode }">
    <!-- Scroll Progress Indicator -->
    <div class="scroll-progress-bar" :style="{ width: scrollProgress + '%' }"></div>
    
    <!-- Theme Controls -->
    <ThemeControls />

    <!-- Hero Section -->
    <section id="hero" class="hero-section">
      <div class="container">
        <div class="hero-content">
          <div class="logo-hero">
            <img src="@/assets/NPC-logo.png" alt="GPD Logo" class="hero-logo" />
          </div>
          <h1 class="hero-title">GPD Reporting System</h1>
          <p class="hero-subtitle">Generation and Performance Division - Agus-Pulangi Hydro-Electric Power Plants</p>
          <p class="hero-tagline">Streamline your power generation reporting with real-time analytics</p>
          
          <div class="cta-buttons">
            <router-link to="/register" class="btn btn-primary">
              <i class="pi pi-user-plus"></i>
              Get Started
            </router-link>
            <router-link to="/login" class="btn btn-secondary">
              <i class="pi pi-sign-in"></i>
              Sign In
            </router-link>
          </div>
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

    <!-- Stats Section -->
    <section id="stats" class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">{{ stats.plants }}</div>
            <div class="stat-label">Power Plants</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.capacity.toLocaleString() }}</div>
            <div class="stat-label">Total Capacity (MW)</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Real-time Monitoring</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.uptime }}%</div>
            <div class="stat-label">System Uptime</div>
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
        <p class="section-subtitle">Real-time monitoring of the GPD Reporting System</p>
        
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
                <textarea v-model="feedbackForm.testimonial" rows="4" placeholder="Share your experience with the GPD Reporting System..." required></textarea>
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

    <!-- Video Demo Section -->
    <section id="video-demo" class="video-demo-section">
      <div class="container">
        <h2 class="section-title">See It In Action</h2>
        <p class="section-subtitle">Watch how the GPD Reporting System simplifies your workflow</p>
        
        <div class="video-container" @click="openVideoModal">
          <div class="video-thumbnail">
            <div class="video-play-button">
              <i class="pi pi-play"></i>
            </div>
            <div class="video-overlay">
              <div class="video-duration">3:45</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Timeline -->
    <section id="timeline" class="timeline-section">
      <div class="container">
        <h2 class="section-title">Our Journey</h2>
        <p class="section-subtitle">Evolution of the GPD Reporting System</p>
        
        <div class="timeline">
          <div 
            v-for="(milestone, index) in timeline" 
            :key="index"
            class="timeline-item"
            :class="{ left: index % 2 === 0, right: index % 2 !== 0 }"
          >
            <div class="timeline-content">
              <div class="timeline-date">{{ milestone.date }}</div>
              <h3>{{ milestone.title }}</h3>
              <p>{{ milestone.description }}</p>
            </div>
            <div class="timeline-dot"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Comparison Table -->
    <section id="comparison" class="comparison-section">
      <div class="container">
        <h2 class="section-title">Before vs After</h2>
        <p class="section-subtitle">See the transformation with GPD Reporting System</p>
        
        <div class="comparison-table">
          <div class="comparison-header">
            <div class="comparison-col"></div>
            <div class="comparison-col before">Before</div>
            <div class="comparison-col after">After</div>
          </div>
          
          <div 
            v-for="(item, index) in comparisonItems" 
            :key="index"
            class="comparison-row"
          >
            <div class="comparison-feature">{{ item.feature }}</div>
            <div class="comparison-value before">
              <i class="pi pi-times"></i>
              {{ item.before }}
            </div>
            <div class="comparison-value after">
              <i class="pi pi-check"></i>
              {{ item.after }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter Signup -->
    <section id="newsletter" class="newsletter-section">
      <div class="container">
        <div class="newsletter-content">
          <div class="newsletter-text">
            <h2>Stay Updated</h2>
            <p>Get the latest updates, features, and announcements delivered to your inbox</p>
          </div>
          <div class="newsletter-form">
            <input 
              v-model="newsletterEmail" 
              type="email" 
              placeholder="Enter your email address"
              @keyup.enter="subscribeNewsletter"
              class="newsletter-input"
            />
            <button @click="subscribeNewsletter" class="newsletter-btn">
              <i class="pi pi-send"></i>
              Subscribe
            </button>
          </div>
          <transition name="fade">
            <div v-if="newsletterSuccess" class="newsletter-success">
              <i class="pi pi-check-circle"></i>
              Thank you for subscribing!
            </div>
          </transition>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section id="faq" class="faq-section">
      <div class="container">
        <h2 class="section-title">Frequently Asked Questions</h2>
        <p class="section-subtitle">Everything you need to know about the GPD Reporting System</p>
        
        <div class="faq-grid">
          <div 
            v-for="(faq, index) in faqs" 
            :key="index"
            class="faq-item"
            :class="{ active: activeFaq === index }"
            @click="toggleFaq(index)"
          >
            <div class="faq-question">
              <h3>{{ faq.question }}</h3>
              <i class="pi" :class="activeFaq === index ? 'pi-minus' : 'pi-plus'"></i>
            </div>
            <transition name="faq-answer">
              <div v-if="activeFaq === index" class="faq-answer">
                <p>{{ faq.answer }}</p>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="how-it-works-section">
      <div class="container">
        <h2 class="section-title">How It Works</h2>
        <p class="section-subtitle">Get started in three simple steps</p>
        
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-icon">
              <i class="pi pi-file-excel"></i>
            </div>
            <h3>Upload Reports</h3>
            <p>Import your daily power generation reports in Excel format</p>
          </div>

          <div class="step-arrow">
            <i class="pi pi-arrow-right"></i>
          </div>

          <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-icon">
              <i class="pi pi-eye"></i>
            </div>
            <h3>View Analytics</h3>
            <p>Monitor real-time data and visualize trends across all plants</p>
          </div>

          <div class="step-arrow">
            <i class="pi pi-arrow-right"></i>
          </div>

          <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-icon">
              <i class="pi pi-file-pdf"></i>
            </div>
            <h3>Generate Summaries</h3>
            <p>Create comprehensive reports for stakeholders and management</p>
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
            <span>Get started with GPD Reporting System today!</span>
          </div>
          <div class="cta-banner-actions">
            <router-link to="/register" class="cta-banner-btn">
              Get Started Free
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
            <img src="@/assets/NPC-logo.png" alt="GPD Logo" class="footer-logo" />
            <p>Generation and Performance Division</p>
            <p class="footer-tagline">Powering Excellence in Reporting</p>
          </div>
          
          <div class="footer-links">
            <div class="footer-column">
              <h4>Product</h4>
              <a href="#">Features</a>
              <a href="#">Documentation</a>
              <a href="#">Support</a>
            </div>
            
            <div class="footer-column">
              <h4>Company</h4>
              <a href="#">About GPD</a>
              <a href="#">Contact Us</a>
              <a href="#">Careers</a>
            </div>
            
            <div class="footer-column">
              <h4>Legal</h4>
              <a href="#">Privacy Policy</a>
              <a href="#">Terms of Service</a>
              <a href="#">Security</a>
            </div>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2026 National Power Corporation. All rights reserved.</p>
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
      videoUrl: '', // Add your video URL here: '/videos/demo.mp4' or 'https://youtube.com/embed/...'
      useYouTube: false, // Set to true if using YouTube embed
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
          description: 'Initial planning and requirements gathering for the GPD Reporting System'
        },
        {
          date: 'Q2 2025',
          title: 'Development Phase',
          description: 'Core features implemented including dashboard, upload, and reporting modules'
        },
        {
          date: 'Q3 2025',
          title: 'Beta Testing',
          description: 'Pilot deployment across 3 power plants with user feedback integration'
        },
        {
          date: 'Q4 2025',
          title: 'Full Launch',
          description: 'System deployed to all 7 Agus-Pulangi power plants'
        },
        {
          date: 'Q1 2026',
          title: 'Enhanced Analytics',
          description: 'Advanced charting and comparison features added based on user requests'
        },
        {
          date: 'Q2 2026',
          title: 'Future Roadmap',
          description: 'AI-powered predictive analytics and mobile app in development'
        }
      ],
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
          question: 'What is the GPD Reporting System?',
          answer: 'The GPD Reporting System is a comprehensive platform designed to streamline the management and reporting of power generation data from the Agus-Pulangi hydroelectric power plants. It provides real-time monitoring, data analytics, and automated report generation for the Generation and Performance Division.'
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
          answer: 'Yes, the GPD Reporting System is fully responsive and optimized for mobile devices. You can access all features including dashboard monitoring, report viewing, and data uploads from your smartphone or tablet.'
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
            text: 'The GPD Reporting System has transformed how we manage daily reports.',
            rating: 5
          }];
        }
      } catch (error) {
        console.error('Error loading testimonials:', error);
        // Fallback to default testimonial if API fails
        this.testimonials = [{
          name: 'GPD User',
          role: 'Power Plant Personnel',
          text: 'The GPD Reporting System has transformed how we manage daily reports.',
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
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  position: relative;
  overflow: hidden;
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
  z-index: 1;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  animation: fadeInUp 1s ease-out;
  transition: transform 0.1s ease-out, opacity 0.1s ease-out;
}

.logo-hero {
  margin-bottom: 30px;
  animation: float 3s ease-in-out infinite;
}

.hero-logo {
  width: 120px;
  height: 120px;
  object-fit: contain;
  filter: drop-shadow(0 4px 20px rgba(59, 130, 246, 0.3));
  transition: transform 0.3s ease;
}

.hero-logo:hover {
  transform: scale(1.1) rotate(5deg);
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  color: white;
  margin: 0 0 20px 0;
  letter-spacing: -0.02em;
  animation: fadeInDown 1s ease-out 0.2s both;
}

.hero-subtitle {
  font-size: 1.5rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 15px 0;
  animation: fadeInDown 1s ease-out 0.4s both;
}

.hero-tagline {
  font-size: 1.125rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 40px 0;
  line-height: 1.6;
  animation: fadeInDown 1s ease-out 0.6s both;
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
  background: #f8fafc;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  text-align: center;
  margin: 0 0 15px 0;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #64748b;
  text-align: center;
  margin: 0 0 60px 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-top: 60px;
}

.feature-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 40px 30px;
  text-align: center;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
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
  width: 80px;
  height: 80px;
  margin: 0 auto 25px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.feature-card:hover .feature-icon {
  transform: rotateY(360deg) scale(1.1);
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
}

.feature-card h3 {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0 0 15px 0;
  font-weight: 600;
  transition: color 0.3s ease;
}

.feature-card:hover h3 {
  color: #3b82f6;
}

.feature-card p {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0;
  transition: color 0.3s ease;
}

.feature-card:hover p {
  color: #475569;
}

/* Stats Section */
.stats-section {
  padding: 80px 20px;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
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
  background: radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
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
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-10px) scale(1.05);
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(59, 130, 246, 0.5);
  box-shadow: 0 20px 40px rgba(59, 130, 246, 0.2);
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
  background: white;
  overflow: hidden;
}

.carousel-container {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  padding: 0 60px;
}

.carousel-track {
  position: relative;
  height: 500px;
  overflow: hidden;
}

.carousel-slide {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transform: translateX(100%) scale(0.8);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
}

.carousel-slide.active {
  opacity: 1;
  transform: translateX(0) scale(1);
  pointer-events: auto;
}

.plant-showcase-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
}

.plant-showcase-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border-color: #3b82f6;
}

.plant-image-placeholder {
  height: 250px;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.plant-image-placeholder::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 50%, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
}

.plant-image-placeholder i {
  font-size: 5rem;
  color: rgba(255, 255, 255, 0.3);
  z-index: 1;
  animation: pulse 3s ease-in-out infinite;
}

.plant-code-overlay {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(59, 130, 246, 0.9);
  backdrop-filter: blur(10px);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
  z-index: 2;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.plant-showcase-content {
  padding: 30px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.plant-showcase-content h3 {
  font-size: 1.75rem;
  color: #1e293b;
  margin: 0 0 20px 0;
  font-weight: 700;
}

.plant-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.plant-detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #64748b;
  font-size: 1rem;
}

.plant-detail-item i {
  color: #3b82f6;
  font-size: 1.125rem;
}

.plant-description {
  color: #64748b;
  line-height: 1.6;
  margin: 0;
  flex: 1;
}

.carousel-btn {
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

.carousel-btn:hover {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
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
  gap: 10px;
  margin-top: 30px;
}

.carousel-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #cbd5e1;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.carousel-indicator:hover {
  background: #94a3b8;
  transform: scale(1.2);
}

.carousel-indicator.active {
  background: #3b82f6;
  width: 32px;
  border-radius: 6px;
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

.footer-logo {
  width: 60px;
  height: 60px;
  object-fit: contain;
  margin-bottom: 10px;
  transition: transform 0.3s ease;
}

.footer-logo:hover {
  transform: scale(1.1) rotate(5deg);
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

.dark-mode .section-title {
  color: white;
}

.dark-mode .section-subtitle {
  color: #94a3b8;
}

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

/* Live Stats Dashboard */
.live-stats-section {
  padding: 100px 20px;
  background: white;
}

.live-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-top: 60px;
}

.live-stat-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 30px;
  display: flex;
  gap: 20px;
  align-items: flex-start;
  transition: all 0.4s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.live-stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #3b82f6 0%, #8b5cf6 100%);
  transform: scaleY(0);
  transition: transform 0.4s ease;
}

.live-stat-card:hover::before {
  transform: scaleY(1);
}

.live-stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
  border-color: #3b82f6;
}

.live-stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: #3b82f6;
  flex-shrink: 0;
  transition: all 0.4s ease;
}

.live-stat-card:hover .live-stat-icon {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  transform: scale(1.1) rotate(5deg);
}

.live-stat-content {
  flex: 1;
}

.live-stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  line-height: 1;
  margin-bottom: 8px;
}

.live-stat-label {
  font-size: 0.9375rem;
  color: #64748b;
  margin-bottom: 10px;
  font-weight: 500;
}

.live-stat-trend {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.875rem;
  font-weight: 600;
}

.live-stat-trend.positive {
  color: #10b981;
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
  padding: 100px 20px;
  background: white;
}

.video-container {
  max-width: 900px;
  margin: 0 auto;
  cursor: pointer;
}

.video-thumbnail {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  transition: all 0.4s ease;
}

.video-thumbnail:hover {
  transform: scale(1.02);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
}

.video-play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.9);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  transition: all 0.4s ease;
  box-shadow: 0 10px 40px rgba(59, 130, 246, 0.5);
}

.video-thumbnail:hover .video-play-button {
  transform: translate(-50%, -50%) scale(1.2);
  background: rgba(59, 130, 246, 1);
}

.video-play-button i {
  margin-left: 8px;
}

.video-overlay {
  position: absolute;
  bottom: 20px;
  right: 20px;
}

.video-duration {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
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
}

.timeline-content:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
  border-color: #3b82f6;
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
  background: white;
}

.comparison-table {
  max-width: 900px;
  margin: 60px auto 0;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.comparison-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  color: white;
  font-weight: 700;
  font-size: 1.125rem;
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
  border-bottom: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.comparison-row:last-child {
  border-bottom: none;
}

.comparison-row:hover {
  background: #f8fafc;
}

.comparison-feature {
  padding: 20px 25px;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
}

.comparison-value {
  padding: 20px 25px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 0.9375rem;
}

.comparison-value.before {
  color: #ef4444;
  background: #fef2f2;
}

.comparison-value.after {
  color: #10b981;
  background: #f0fdf4;
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
