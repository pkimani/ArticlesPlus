# ArticlesPlus

ArticlesPlus is a full-stack web application designed to aggregate, display, and rank news article titles. Built with Django, Next.js, and React.js, and utilizing technologies like uWSGI, Nginx, PostgreSQL, Celery, RabbitMQ, OpenAI API, and SSL, ArticlesPlus offers a robust and scalable platform for news curation. The application showcases article titles in a responsive, masonry-style layout and supports customizable color themes including light mode, dark mode, yellow, green, and pink, catering to user preferences for a more personalized browsing experience.

## Features

- **News Article Aggregation**: Dynamically fetches and updates news articles using RSS feeds.
- **Intelligent Ranking**: Leverages the OpenAI API to analyze and rank articles based on relevance and quality.
- **Customizable Themes**: Users can choose between various color themes for a personalized browsing experience.
- **Responsive Layout**: Employs React.js and Masonry layout for a fluid, responsive design across different screen sizes.
- **Secure Communication**: Uses self-signed SSL certificates for localhost to ensure encrypted data transmission.
- **Efficient Background Tasks**: Utilizes Celery workers with RabbitMQ for asynchronous task processing, enhancing the application's performance and scalability.
- **Professional Deployment**: Leverages uWSGI and Nginx for a robust, production-ready deployment, avoiding the need for development servers.

## Getting Started

### Prerequisites

This project is developed and tested in the following environment:
- Ubuntu Linux 22.04.4 LTS
- Python 3.10.12
- Node.js 10.2.5

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pkimani/ArticlesPlus.git
   cd ArticlesPlus
   ```

2. **Backend Setup (Django)**
   - Ensure you have Python 3.10 and virtualenv installed.
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Migrate the database:
     ```bash
     python manage.py migrate
     ```

3. **Frontend Setup (Next.js)**
   - Navigate to the Next.js project directory:
     ```bash
     cd djrssproj-next
     ```
   - Install Node.js dependencies:
     ```bash
     npm install
     ```
   - Build and start the Next.js production server:
     ```bash
     npm run build
     npm start
     ```

4. **uWSGI and Nginx Configuration**
   - Follow the guides provided in `/Configuration/Nginx` and `/Configuration/uWSGI` to configure uWSGI and Nginx for serving the Django application.

5. **Environment Variables**
   - Set up the necessary environment variables in `Configuration/environment_variables`:
     ```
     DJANGO_SECRET_KEY=your_secret_key
     OPENAI_API_KEY=your_openai_api_key
     POSTGRES_PASSWORD=your_postgres_password
     ```

6. **Generate SSL Certificates**
   - Follow steps to generate self-signed SSL certificates for localhost, ensuring secure communication during development.

### Usage

Access the web application by navigating to the configured domain/URL in your web browser.

## Customizing Themes

To change the theme, navigate to the settings within the web interface and select your preferred theme from the available options.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for how you can contribute to ArticlesPlus.

## License

This project is licensed under the GPL License - see the LICENSE file for details.

## Acknowledgments

- OpenAI API for the AI-driven analysis capabilities.
- The Django and Next.js communities for the foundational frameworks.
- Celery and RabbitMQ for background task processing solutions.
