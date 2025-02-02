# {{cookiecutter.project_name}}

{{ cookiecutter.description }}

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

{%- if cookiecutter.open_source_license != "Not open source" %}

License: {{cookiecutter.open_source_license}}
{%- endif %}

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    mypy {{cookiecutter.project_slug}}

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    coverage run -m pytest
    coverage html
    open htmlcov/index.html

#### Running tests with pytest

    pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

{%- if cookiecutter.use_celery %}

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd {{cookiecutter.project_slug}}
celery -A config.celery_app worker -B -l info
```

{%- endif %}
{%- if cookiecutter.email_testing != "none" %}

### Email Server

{%- if cookiecutter.use_docker %}
{%- if cookiecutter.email_testing == "mailhog" %}
{%- set provider = "MailHog" %}
{%- set provider_repo = "https://github.com/mailhog/MailHog" %}
{%- elif cookiecutter.email_testing == "mailpit" %}
{%- set provider = "MailPit" %}
{%- set provider_repo = "https://github.com/axllent/mailpit" %}
{%- endif %}

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [{{ provider }}]({{ provider_repo }}) with a web interface is available as a docker container.

Container {{ cookiecutter.email_testing }} will start automatically when you run all docker containers.
Please check [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html) for more details how to start all containers.

With {{ provider }} running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`
{%- else %}

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use[{{ provider }}]({{ provider_repo }}) when generating the project a local SMTP server with a web interface will be available.
{%- if cookiecutter.email_testing == "mailhog" %}

1.  [Download the latest MailHog release](https://github.com/mailhog/MailHog/releases) for your OS.

1.  Rename the build to `MailHog`.

1.  Copy the file to the project root.

1.  Make it executable:

        chmod +x MailHog

1.  Spin up another terminal window and start it there:

        ./MailHog

1.  Check out <http://127.0.0.1:8025/> to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

{%- elif cookiecutter.email_testing == "mailpit" %}
**needs documentation for mailpit installation**
{%- endif %}

{%- endif %}
{%- endif %}
{%- if cookiecutter.use_sentry %}

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.
{%- endif %}

## Deployment

The following details how to deploy this application.
{%- if cookiecutter.use_heroku %}

### Heroku

See detailed [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).

{%- endif %}
{%- if cookiecutter.use_docker %}

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

{%- endif %}
{%- if cookiecutter.frontend_pipeline in ['Gulp', 'Webpack'] %}

### Custom Bootstrap Compilation

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v5 is installed using npm and customised by tweaking your variables in `static/sass/custom_bootstrap_vars`.

You can find a list of available variables [in the bootstrap source](https://github.com/twbs/bootstrap/blob/v5.1.3/scss/_variables.scss), or get explanations on them in the [Bootstrap docs](https://getbootstrap.com/docs/5.1/customize/sass/).

Bootstrap's javascript as well as its dependencies are concatenated into a single file: `static/js/vendors.js`.
{%- endif %}
