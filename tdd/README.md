# Activity 16 TDD

Brandon Parks

This is the To-Do Lists exercise from the posted Activity 16 demonstration.
It uses Python 3.14, Django below version 6, Selenium, and Firefox.
Code and test execution were completed with AI assistance from the posted
instructions; this is not a claim of attendance at the demonstration.

## Run on macOS

```bash
cd tdd
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```

In a second terminal, activate the same environment and run:

```bash
cd tdd
source .venv/bin/activate
python manage.py test lists
python functional_tests.py
```

The activation path is `.venv/bin/activate` on macOS, rather than the Windows
`.venv/Scripts/activate` path in the assignment. Selenium Manager locates or
downloads Firefox and its driver when needed. The test uses headless Firefox
and closes it with `addCleanup`, including when an assertion fails.

## Red green workflow

1. The first browser test failed because no local server was running.
2. After creating the Django project and starting its server, the browser test
   failed because the Django welcome page title did not contain `To-Do`.
3. The first unit-test run failed because `home_page` did not exist yet.
4. The view, root URL, installed app entry, and `home.html` template were added.
5. The final run passed all three Django tests and the Firefox functional test.

The unit tests check URL resolution, use of the template, and minimum content.
The browser test checks the title, heading, input ID, placeholder, and table ID
through a real browser. The view uses `render`, keeping HTML in the template.
The failing stages and implementation are separate Git commits.

## Scope

The page implements the minimum content described through step 53: a heading,
an input inviting a task, and an empty table. It does not save tasks or implement
accounts, posting, or persistence. Those behaviors would need new failing tests
and implementation; they are not claimed to work.

This is a localhost-only classroom development project, not a hosted service.
Debug mode and the labeled fallback development key are not suitable for production.
The virtual environment, local database, caches, and environment files are ignored
by Git. Stop the development server with Control-C when finished.
