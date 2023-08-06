from distutils.core import setup
setup(
  name = 'ybc_face_ps',
  packages = ['ybc_face_ps'],
  # package_data = {'ybc_face':['data/*']},
  version = '4.0.7',
  description = 'Face Control',
  long_description='Face Control',
  author = 'KingHS',
  author_email = '382771946@qq.com',
  keywords = ['pip3', 'python3','python','Face Info'],
  license='MIT',
  # install_requires=['requests','opencv-python','pillow']
  install_requires=['requests','pillow']
)
