import baseConfig from '@acme/eslint-config/base'

/** @type {import('typescript-eslint').Config} */
export default [
  {
    ignores: [],
  },
  ...baseConfig,
  {
    '@typescript-eslint/ no-unsafe-assignment': 'off',
  },
]
