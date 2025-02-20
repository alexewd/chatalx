# chatalx

# Contributing to the Project

Thank you for considering contributing to our project! We appreciate your help and support. Please follow the guidelines below to ensure a smooth collaboration.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Setting Up Your Environment

To work with this repository, please ensure you have Git installed on your machine. You can download it from [git-scm.com](https://git-scm.com/).

### Handling File Names with Non-ASCII Characters

This project contains files with names in Russian. To avoid issues with displaying these file names, please follow these steps:

1. **Configure Git to Handle Non-ASCII Characters**:
   To ensure that you can see the file names correctly, you may need to change your Git configuration. Run the following command in your terminal:

   ```bash
   git config --global core.quotepath false
This setting will allow Git to display file names with non-ASCII characters (like Russian) correctly.

Ensure Your Terminal Supports UTF-8: Make sure that your terminal or command prompt is set to use UTF-8 encoding. This will help in displaying the file names properly.
Making Changes
Fork the Repository: Click the "Fork" button on the top right of the repository page to create your own copy of the repository.
Clone Your Fork: Clone your forked repository to your local machine:

git clone https://github.com/your-username/repository-name.git
Create a New Branch: Before making changes, create a new branch:

git checkout -b your-feature-branch
Make Your Changes: Edit the files as needed. If you are working with files that have Russian names, ensure that your environment is set up as mentioned above.
Commit Your Changes: Once you are done, commit your changes:

git add .
git commit -m "Description of your changes"
Push Your Changes: Push your changes to your forked repository:

git push origin your-feature-branch
Create a Pull Request: Go to the original repository and create a pull request from your branch.
Questions or Issues
If you have any questions or run into issues, feel free to open an issue in the repository or reach out to the maintainers.

Thank you for contributing!
