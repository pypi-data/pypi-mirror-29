# pythonagent-tcell [![Build Status](https://travis-ci.com/tcellio/pythonagent-tcell.svg?token=CtepHZ2QyME9hgobedQx&branch=master)](https://travis-ci.com/tcellio/pythonagent-tcell)

A tCell.io security agent that instruments your python projects

What does it do?  ...

###How do I get it?
1. If you have a virtualenv for your project, activate it. (recommended so you don't need to install packages as root)

2. You can use pip (not yet supported) or a manual build
  ``` sh
  ~/projects> pip install tcell_agent (not yet published)
  ```

  or
  ```
  ~/projects> git clone https://github.com/tcellio/pythonagent-tcell.git
  ~/projects> pip install -e ./pythonagent-tcell
  ```

### Run the app
3. Switch to your project
  ``` sh
  ~/projects> cd mydjango/
  ```

4. Add the config file you downloaded from the agents page to your projects root directory (tcell_agent.config)

5. Start your project using the tcell_agent, logs will be available in logs/tcell_agent.log

  If you previously used
  ``` sh
  ~/projects/pythonagent-tcell> python manage.py runserver 0.0.0.0:8000
  ```

  now use
  ``` sh
  ~/projects/pythonagent-tcell> tcell_agent run python manage.py runserver 0.0.0.0:8000
  ```

### Contributing

1. Install Dependencies

  ``` sh
  ~/projects/pythonagent-tcell> pip install -r requirements.txt
  ```

2. Run Tests

  ``` sh
  ~/projects/pythonagent-tcell> python -m nose
  ```
