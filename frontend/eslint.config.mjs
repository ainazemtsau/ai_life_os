import js from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";
import importPlugin from "eslint-plugin-import";
import unusedImports from "eslint-plugin-unused-imports";
import unicorn from "eslint-plugin-unicorn";
import sonarjs from "eslint-plugin-sonarjs";
import eslintConfigPrettier from "eslint-config-prettier";

export default [
  {
    ignores: [
      "eslint.config.mjs",
      "next-env.d.ts",
      "tailwind.config.ts",
      "postcss.config.mjs",
      "components.json",
      ".next/**",
      "node_modules/**",
      ".vercel/**",
      ".turbo/**",
      "dist/**",
      "build/**",
      "coverage/**",
    ],
  },

  js.configs.recommended,

  ...tseslint.configs.recommended,

  {
    files: ["**/*.{js,jsx,ts,tsx}"],
    languageOptions: {
      globals: { ...globals.browser, ...globals.node },
    },
    plugins: {
      react,
      "react-hooks": reactHooks,
      "jsx-a11y": jsxA11y,
      import: importPlugin,
      "unused-imports": unusedImports,
      unicorn,
      sonarjs,
    },
    rules: {
      complexity: ["error", 8],
      "max-lines": ["warn", { max: 300, skipBlankLines: true, skipComments: true }],
      "max-params": ["warn", 4],
      "sonarjs/no-duplicate-string": "warn",
      "@typescript-eslint/consistent-type-imports": ["error", { prefer: "type-imports" }],
      "@typescript-eslint/no-explicit-any": "warn",
      "unused-imports/no-unused-imports": "error",
      "import/order": [
        "error",
        {
          groups: ["builtin", "external", "internal", ["parent", "sibling", "index"]],
          pathGroups: [
            { pattern: "react", group: "external", position: "before" },
            { pattern: "@/**", group: "internal", position: "after" },
          ],
          pathGroupsExcludedImportTypes: ["react"],
          "newlines-between": "always",
          alphabetize: { order: "asc", caseInsensitive: true },
        },
      ],
      "react/react-in-jsx-scope": "off",
      "react/jsx-key": "error",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
      "unicorn/no-abusive-eslint-disable": "error",
      "unicorn/prefer-query-selector": "error",
    },
  },

  {
    files: ["src/**/*.{ts,tsx}"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        projectService: true,
        tsconfigRootDir: process.cwd(),
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
    },
    rules: {
      "@typescript-eslint/await-thenable": "error",
      "@typescript-eslint/no-floating-promises": ["error", { ignoreVoid: false }],
      "@typescript-eslint/no-misused-promises": [
        "error",
        { checksVoidReturn: { attributes: false } },
      ],
      "@typescript-eslint/no-unsafe-assignment": "warn",
      "@typescript-eslint/no-unsafe-call": "warn",
      "@typescript-eslint/no-unsafe-member-access": "warn",
      "@typescript-eslint/no-unsafe-argument": "warn",
      "@typescript-eslint/restrict-template-expressions": [
        "warn",
        { allowNumber: true, allowBoolean: true },
      ],
      "@typescript-eslint/require-await": "error",
      "@typescript-eslint/unbound-method": ["error", { ignoreStatic: true }],
    },
  },

  {
    files: ["**/*.test.{ts,tsx}", "**/__tests__/**/*.{ts,tsx}"],
    rules: {
      "@typescript-eslint/no-floating-promises": "off",
      "@typescript-eslint/no-unsafe-assignment": "off",
      "@typescript-eslint/no-unsafe-call": "off",
      "@typescript-eslint/no-unsafe-member-access": "off",
      "@typescript-eslint/no-unsafe-argument": "off",
      "max-lines": "off",
    },
  },

  eslintConfigPrettier,
];
