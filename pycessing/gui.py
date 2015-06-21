from javax.swing import JFrame, JPanel, JButton, BorderFactory
from java.awt import GridLayout
from java.awt.event import KeyEvent


def create(reload_func, exit_func):
  def restart_app(event):
    reload_func()
    # reload_sketch()

  def exit_app(event):
    exit_func()
    # system_vars.system_requests.append({'command': 'exit'})

  def check_exit(event):
    if event.getKeyCode() == KeyEvent.VK_ESCAPE:
      exit_func()
      # system_vars.system_requests.append({'command': 'exit'})

  frame = JFrame('Pycessing', defaultCloseOperation=JFrame.EXIT_ON_CLOSE, size=(240, 80))

  frame.setResizable(False)
  frame.setLocationByPlatform(True)

  panel = JPanel()
  panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10))
  panel.setLayout(GridLayout(1, 2, 8, 8))

  restart_button = JButton('Restart', actionPerformed=restart_app, keyPressed=check_exit)
  panel.add(restart_button)

  exit_button = JButton('Exit', actionPerformed=exit_app, keyPressed=check_exit)
  panel.add(exit_button)

  frame.add(panel)

  frame.setVisible(True)
