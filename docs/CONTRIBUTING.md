## Contributing Guidelines

To ensure a smooth and consistent workflow, please follow these guidelines.


### Workflow

1. **Branching:**

   - **Main Branch:** The `main` branch contains stable, production-ready code. Do not commit directly to this branch.
   - **Feature Branches:** Create a new branch for each feature or bug fix. Use a naming convention like `feature/feature-name` or `bugfix/issue-description`.
     - Example: `feature/user-authentication` or `bugfix/fix-login-error`
   - **Hotfix Branches:** For urgent fixes to the production code, create a `hotfix/` branch.
     - Example: `hotfix/security-patch`

2. **Commit Messages:**

   - Use clear and descriptive commit messages.
   - Follow the [conventional commits](https://www.conventionalcommits.org/) style:
     - `feat`: A new feature
     - `fix`: A bug fix
     - `docs`: Documentation only changes
     - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
     - `refactor`: A code change that neither fixes a bug nor adds a feature
     - `test`: Adding missing tests or correcting existing tests

3. **Pull Requests:**

   - Ensure your branch is up to date with the `develop` branch before submitting a pull request.
   - Provide a clear description of the changes and any related issues.
   - Request a review from at least one other team member.
   - Address any feedback and make necessary changes before merging.

   
### Code Quality

For frontend:

- Please ensure your code adheres to the coding standards by running the following commands before committing:

  ```bash
  npm run lint:check
  npm run lint:fix
  ```

For backend:

- Install [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) on VScode extension
- Run Pylint to check for code quality issues and adhere to Python coding standards.


### Testing

- Write unit tests for new features and bug fixes.
- Ensure all tests pass before submitting a pull request.
- Use a consistent testing framework (e.g., Jest for frontend, Pytest for backend).

### Documentation

- Update documentation for any new features or changes.
- Ensure the `README.md` and other relevant documentation files are up to date.