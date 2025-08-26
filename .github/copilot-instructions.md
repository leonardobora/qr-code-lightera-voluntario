# GitHub Copilot Instructions - QR Code Lightera Voluntário

## Project Overview

This is a **QR Code Management System** for the Lightera Voluntário organization. The system generates and manages QR codes for different volunteer activities including events (festas), donation baskets (cestas), toys (brinquedos), and school materials (material escolar).

### Purpose
- Generate QR codes for tracking volunteer activities and donations
- Provide administrative interface for volunteer coordinators
- Enable mobile-friendly scanning and validation
- Generate usage reports for organizational insights

## Tech Stack

### Backend
- **Python 3.8+**: Primary language
- **Flask**: Web framework for backend APIs and web interface
- **SQLite**: Local database for development and small deployments
- **qrcode**: Python library for QR code generation
- **Pillow (PIL)**: Image processing for QR code customization

### Frontend
- **HTML5**: Semantic markup
- **Bootstrap 5**: Responsive CSS framework
- **HTML5-QRCode**: JavaScript library for browser-based QR scanning
- **Vanilla JavaScript**: For interactive features

### Development Tools
- **pandas**: Data analysis for feasibility studies
- **plotly**: Visualization for architectural analysis

## Code Style Guidelines

### Python Code Style
- Follow **PEP 8** conventions
- Use **type hints** for all function parameters and return values
- Include **docstrings** for all functions, classes, and modules
- Maximum line length: 88 characters (Black formatter compatible)

```python
def generate_qr_code(data: str, event_type: str) -> str:
    """
    Generate QR code for volunteer events.
    
    Args:
        data: Data to encode in QR code
        event_type: Type of event ('festa', 'cesta', 'brinquedo', 'material_escolar')
    
    Returns:
        Base64 encoded QR code image
    """
    pass
```

### HTML/CSS Style
- Use **BEM methodology** for CSS class naming
- Follow semantic HTML5 structure
- Ensure mobile-first responsive design
- Use Bootstrap 5 utility classes when appropriate

```html
<div class="qr-generator">
  <div class="qr-generator__form">
    <button class="qr-generator__submit btn btn-primary">Gerar QR Code</button>
  </div>
</div>
```

## Key Features & Functionality

### Core Features
1. **QR Code Generation**
   - Event QR codes (festas)
   - Donation basket tracking (cestas)
   - Toy distribution (brinquedos)
   - School material distribution (material escolar)

2. **Administrative Interface**
   - Volunteer coordinator dashboard
   - QR code management
   - Usage statistics and reports

3. **Mobile Scanner Interface**
   - Browser-based QR scanning
   - Validation and verification
   - Offline capability considerations

4. **Database Management**
   - Event tracking
   - Volunteer registration
   - Distribution records

## Security Guidelines

### Input Validation
- Sanitize all user inputs before processing
- Validate QR code data format and content
- Implement proper SQL injection prevention

```python
def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent XSS and injection attacks."""
    # Remove HTML tags, validate format
    pass
```

### Authentication & Authorization
- Implement session management for admin interface
- Use CSRF protection for all forms
- Rate limiting for QR generation endpoints

### Data Protection
- Encrypt sensitive volunteer information
- Implement proper access logging
- Follow LGPD (Brazilian data protection) compliance

## Performance Guidelines

### Caching Strategy
- Cache generated QR codes to avoid regeneration
- Use Redis or in-memory caching for frequently accessed data
- Implement proper cache invalidation

### Database Optimization
- Use database indexes for frequently queried fields
- Implement pagination for large datasets
- Consider read replicas for reporting queries

### Async Operations
- Use async/await for I/O operations when possible
- Implement background tasks for heavy QR generation
- Consider task queues for batch operations

```python
async def bulk_generate_qr_codes(event_data: List[Dict[str, str]]) -> List[str]:
    """Generate multiple QR codes asynchronously."""
    pass
```

## Common Patterns

### QR Code Generation Pattern
```python
import qrcode
from io import BytesIO
import base64

def create_event_qr(event_id: str, event_type: str) -> str:
    """Standard QR code generation for events."""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_data = f"lightera://{event_type}/{event_id}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()
```

### API Response Pattern
```python
from flask import jsonify

def api_response(success: bool, data: Dict, message: str = "") -> Response:
    """Standard API response format."""
    return jsonify({
        "success": success,
        "data": data,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })
```

### Database Query Pattern
```python
def get_event_by_id(event_id: str) -> Optional[Dict]:
    """Standard database query with error handling."""
    try:
        # Database query logic
        pass
    except Exception as e:
        logger.error(f"Database error: {e}")
        return None
```

### Form Validation Pattern
```python
def validate_event_form(form_data: Dict[str, str]) -> Tuple[bool, List[str]]:
    """Validate event creation form."""
    errors = []
    
    if not form_data.get('event_name'):
        errors.append("Nome do evento é obrigatório")
    
    if not form_data.get('event_type') in ['festa', 'cesta', 'brinquedo', 'material_escolar']:
        errors.append("Tipo de evento inválido")
    
    return len(errors) == 0, errors
```

## Testing Guidelines

### Unit Tests
- Test all QR generation functions
- Mock external dependencies
- Test edge cases and error conditions

### Integration Tests
- Test API endpoints end-to-end
- Validate QR code scanning workflow
- Test database operations

### Browser Testing
- Test QR scanning on different devices
- Validate responsive design
- Cross-browser compatibility testing

## File Structure

```
qr-code-lightera-voluntario/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
├── tests/
├── config/
├── requirements.txt
└── run.py
```

## Development Workflow

1. **Feature Development**
   - Create feature branch from main
   - Implement with comprehensive tests
   - Follow code style guidelines
   - Create pull request with description

2. **Code Review**
   - Ensure security best practices
   - Validate test coverage
   - Check performance implications
   - Verify responsive design

3. **Deployment**
   - Test in staging environment
   - Validate QR scanning functionality
   - Monitor performance metrics
   - Deploy to production

## Specific Copilot Guidelines

When generating code for this project:

1. **Always include error handling** for QR operations
2. **Consider mobile users** in UI suggestions
3. **Include logging** for debugging volunteer activities
4. **Validate Portuguese language** content appropriately
5. **Consider offline scenarios** for mobile usage
6. **Include accessibility features** for volunteer coordinators
7. **Implement proper sanitization** for user-generated content
8. **Follow Flask best practices** for route organization
9. **Consider database migration** patterns for schema changes
10. **Include proper documentation** in Portuguese when appropriate

## Context-Specific Notes

- This system serves Brazilian volunteer organizations
- Consider Portuguese language in user-facing messages
- Volunteer coordinators may have varying technical expertise
- Mobile usage is primary for field volunteers
- Internet connectivity may be intermittent during events
- Data privacy is crucial for volunteer information
- System should be cost-effective for non-profit usage