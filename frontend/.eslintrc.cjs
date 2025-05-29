module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier', // Make sure this is last to override other formatting rules
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh', 'prettier'],
  rules: {
    'prettier/prettier': 'warn', // Show Prettier issues as warnings
    'react/jsx-uses-react': 'off', // Not needed for React 17+
    'react/react-in-jsx-scope': 'off', // Not needed for React 17+
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-explicit-any': 'warn' // Allow 'any' but show a warning
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
};
