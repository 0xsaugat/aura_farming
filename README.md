# AURA - Nepal Trust Analytics & Carbon Verification Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django 4.0+](https://img.shields.io/badge/Django-4.0+-darkgreen.svg)](https://www.djangoproject.com/)

## 🌍 Project Overview

**AURA (Advanced Unsupervised Recognition and Analytics)** is an AI-powered platform designed to detect, verify, and monetize environmental impact through tree detection, carbon tracking, and blockchain-based verification. Built for the **Embark College AI Hackathon**, AURA-Nepal enables users to upload geotagged media (photos/videos), automatically detect trees and vegetation using AI, calculate carbon credits, and participate in verified environmental finance markets.

The platform bridges the gap between environmental action and financial incentives by providing transparent, AI-verified carbon credit tracking for individuals, researchers, and corporate buyers.

## ✨ Key Features

- **🎥 Smart Media Intake**: Upload geotagged photos and videos with location-based metadata (province, district, coordinates)
- **🤖 AI-Powered Tree Detection**: Leverages Hugging Face transformers (YOLO, Vision models) for automatic tree and vegetation detection in satellite imagery and ground photos
- **📊 Real-Time Analytics**: Dashboard displaying Carbon records, detection statistics, and environmental impact metrics
- **✅ Verification Ledger**: Immutable records of all detections and carbon validations for transparency
- **💰 Finance Transactions**: Track carbon credits, pricing, and transactions between verifiers and corporate buyers
- **👥 Role-Based Access Control**: Granular permissions for Admins, Researchers, Uploaders, and Corporate Buyers
- **🗺️ Geographic Intelligence**: Location-aware processing with province/district-level organization
- **🔐 Secure Access**: Login-protected endpoints with user authentication and authorization

## 🛠️ Tech Stack

### Backend

- **Framework**: Django 4.0+ (Python 3.10+)
- **Database**: SQLite (MVP) / PostgreSQL + PostGIS (production-ready)
- **AI/ML**:
  - **Hugging Face Transformers** - State-of-the-art pre-trained models for object detection and image classification
  - **YOLO Integration** - Real-time tree detection in video/image streams
  - **Vision Models** - Semantic segmentation for vegetation mapping
- **Task Queue**: Celery (scalable async processing)
- **API**: Django REST Framework (optional)

### Frontend

- **Template Engine**: Django Templates with Bootstrap
- **Geolocation**: Leaflet.js for interactive maps
- **Data Visualization**: Chart.js, D3.js

## 📋 Project Structure

```
aura_farming/
├── core/                    # Django project settings & root configuration
│   ├── settings.py          # Project-wide configuration
│   ├── urls.py              # Root URL dispatcher
│   └── wsgi.py              # WSGI application
├── app/                     # Main backend application
│   ├── models.py            # Core data models
│   ├── views.py             # Request handlers
│   ├── forms.py             # Django forms
│   ├── services.py          # Business logic & AI integration
│   ├── urls.py              # App URL routes
│   ├── admin.py             # Django admin configuration
│   └── migrations/          # Database schema changes
├── analyzer/                # Optional AI analysis module
│   ├── models.py
│   ├── views.py
│   └── services.py
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── app/                 # App-specific templates
│       ├── landing_page.html
│       ├── secure_access_login.html
│       ├── data_intake_upload.html
│       ├── nepal_trust_map.html
│       ├── sovereign_dashboard.html
│       ├── trust_analytics.html
│       └── verified_finance.html
├── media/                   # User uploads & processed media
└── manage.py                # Django management script
```

## 📦 Core Data Models

### UserProfile

- One-to-one relationship with Django User
- Role-based access: Admin, Researcher, Uploader, Corporate Buyer
- Organization affiliation

### MediaUpload

- Stores uploaded photos/videos with metadata
- Geolocation tracking (latitude, longitude)
- Administrative divisions (province, district)
- Processing status tracking (uploaded → processing → processed)

### TreeDetection

- AI-generated detection results from Hugging Face models
- Bounding box coordinates and confidence scores
- Species classification

### CarbonRecord

- Carbon footprint calculations based on detected trees
- Carbon credit allocation

### VerificationLedger

- Immutable audit trail of all validations
- Timestamp and verifier information

### FinanceTransaction

- Carbon credit trading between users
- Corporate buyer marketplace transactions

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip / Poetry
- Virtual environment tool (venv, conda, etc.)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/aura_farming.git
   cd aura_farming
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Hugging Face API**

   ```bash
   # Set your Hugging Face API token in environment variables
   export HUGGINGFACE_API_KEY="your_api_token_here"
   ```

   Or create a `.env` file:

   ```
   HUGGINGFACE_API_KEY=your_api_token_here
   SECRET_KEY=your_django_secret_key
   DEBUG=True  # Set to False in production
   ```

5. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000/` to access the application.

## 🔌 AI Integration with Hugging Face

The platform integrates Hugging Face transformers for intelligent tree detection and environmental analysis:

### Supported Models

- **Object Detection**: `facebook/detr-resnet-50` - General object detection
- **Tree Detection**: Fine-tuned YOLO models for vegetation/tree detection
- **Image Classification**: Vision Transformers for environmental classification

### Example Usage

```python
from transformers import pipeline
from app.services import TreeDetectionService

# Initialize Hugging Face inference pipeline
detection_pipeline = pipeline(
    "object-detection",
    model="facebook/detr-resnet-50"
)

# Process uploaded media
service = TreeDetectionService()
results = service.detect_trees_in_image(image_path)

# Results include: bounding boxes, species, confidence scores
```

### Key Features

- **Zero-shot Classification**: Classify vegetation without task-specific training
- **Batch Processing**: Process multiple images asynchronously with Celery
- **Model Caching**: Efficient model loading and inference
- **Confidence Scoring**: Probabilistic detection validation

## 📊 API Endpoints

| Endpoint                 | Method   | Description                     |
| ------------------------ | -------- | ------------------------------- |
| `/`                      | GET      | Landing page                    |
| `/login/`                | GET/POST | Secure user authentication      |
| `/upload/`               | GET/POST | Media intake form & file upload |
| `/map/`                  | GET      | Geographic map view             |
| `/dashboard/`            | GET      | Analytics dashboard             |
| `/analytics/`            | GET      | JSON analytics data             |
| `/finance/transactions/` | GET      | Finance transaction history     |
| `/admin/`                | GET      | Django admin interface          |

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

Run specific test module:

```bash
python manage.py test app.tests
python manage.py test analyzer.tests
```

## 📈 Analytics & Reporting

The platform provides real-time analytics including:

- Total trees detected
- Carbon credits generated
- Geographic distribution of uploads
- User engagement metrics
- Transaction history

Access via the **Trust Analytics** dashboard or JSON API endpoint.

## 🔒 Security & Authentication

- Django's built-in user authentication system
- Role-based access control (RBAC) via UserProfile
- CSRF protection on all forms
- SQL injection prevention via ORM
- Secure file upload handling with type validation

## 🌟 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL certificates
- [ ] Set up Celery workers for async tasks
- [ ] Configure Hugging Face API for production inference
- [ ] Use environment variables for secrets
- [ ] Set up database backups

### Deploy with Docker

```dockerfile
# See Dockerfile in repository for containerized deployment
docker build -t aura-farming .
docker run -p 8000:8000 aura-farming
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guide
- Write descriptive commit messages
- Include unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 👥 Team & Credits

**Developed for**: Embark College AI Hackathon  
**Project Name**: AURA (Advanced Unsupervised Recognition and Analytics) - Nepal  
**Technology Partner**: Hugging Face (AI/ML Models)

## 📞 Support & Contact

For issues, feature requests, or questions:

- Open an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: [docs link]

## 🗺️ Roadmap

- [ ] Real-time video stream processing
- [ ] Mobile app for field workers
- [ ] Blockchain-based verification records
- [ ] Multi-language support (Nepali, English)
- [ ] Integration with satellite imagery APIs
- [ ] Advanced carbon credit marketplace
- [ ] ML model fine-tuning pipeline
- [ ] API rate limiting & monitoring
- [ ] E2E encryption for sensitive data

---

**Made with ❤️ for environmental impact and sustainable development.**
