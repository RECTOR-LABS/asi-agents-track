# TypeScript Type-Check Scripts Guide

## Available Scripts

### Basic Type Checking

```bash
npm run type-check
```
**Purpose**: Quick type validation without compilation
**Flags**: `--noEmit`
**Use Case**: Fast type checking during development

### Watch Mode

```bash
npm run type-check:watch
```
**Purpose**: Continuous type checking as you code
**Flags**: `--noEmit --watch`
**Use Case**: Keep running in terminal while developing

### Strict Type Checking (Recommended for Production)

```bash
npm run type-check:strict
```
**Purpose**: Maximum type safety with all strict flags
**Flags**:
- `--noEmit` - Don't emit compiled files
- `--strict` - Enable all strict type checking options
- `--noUnusedLocals` - Report unused local variables
- `--noUnusedParameters` - Report unused function parameters
- `--noUncheckedIndexedAccess` - Add undefined to unverified index signatures
- `--noImplicitReturns` - Ensure all code paths return a value
- `--noFallthroughCasesInSwitch` - Prevent fallthrough in switch statements

**Use Case**: Before commits, PR reviews, CI/CD pipeline

### Combined Scripts

```bash
npm run type-check:all
```
**Purpose**: Run linting + basic type checking
**Use Case**: Quick validation before git push

```bash
npm run type-check:all:strict
```
**Purpose**: Run linting + strict type checking
**Use Case**: Comprehensive validation before PR

### Full Validation

```bash
npm run validate
```
**Purpose**: Type check + lint + build
**Use Case**: Final validation before deployment

## Workflow Recommendations

### During Development
```bash
# Terminal 1: Dev server
npm run dev

# Terminal 2: Type checking
npm run type-check:watch
```

### Before Committing
```bash
npm run type-check:all
```

### Before Pull Request
```bash
npm run type-check:strict
# or
npm run validate
```

### CI/CD Pipeline
```bash
npm run validate
```

## Fixing Common Issues

### Unused Variables
If `type-check:strict` reports unused variables:
```typescript
// ❌ Error: 'foo' is declared but never used
const foo = 'bar';

// ✅ Fix: Remove or use the variable
const foo = 'bar';
console.log(foo);

// ✅ Alternative: Prefix with underscore if intentionally unused
const _foo = 'bar'; // Acknowledges it's unused
```

### Implicit Returns
```typescript
// ❌ Error: Not all code paths return a value
function getValue(x: number) {
  if (x > 0) {
    return x;
  }
  // Missing return for else case
}

// ✅ Fix: Ensure all paths return
function getValue(x: number): number {
  if (x > 0) {
    return x;
  }
  return 0; // Default return
}
```

### Unchecked Indexed Access
```typescript
// ❌ Error: Element implicitly has 'any' type
const arr = ['a', 'b', 'c'];
const value = arr[5]; // Could be undefined

// ✅ Fix: Check for undefined
const value = arr[5];
if (value !== undefined) {
  console.log(value.toUpperCase());
}

// ✅ Alternative: Use optional chaining
console.log(arr[5]?.toUpperCase());
```

## Integration with Pre-commit Hooks

Add to `.husky/pre-commit`:
```bash
#!/bin/sh
npm run type-check:all
```

## Integration with GitHub Actions

Add to `.github/workflows/ci.yml`:
```yaml
- name: Type Check
  run: npm run type-check:strict

- name: Full Validation
  run: npm run validate
```

## Performance Tips

- **Use `type-check:watch` during development** - Faster than running manually
- **Run `type-check` frequently** - Catch errors early
- **Run `type-check:strict` before commits** - Ensure code quality
- **Cache `.next` folder in CI** - Faster builds

## Troubleshooting

### Script Not Working?
```bash
# Ensure TypeScript is installed
npm list typescript

# Reinstall dependencies
npm run clean:all && npm install

# Check tsconfig.json exists
cat tsconfig.json
```

### Too Many Errors?
Start with basic type-check and gradually fix issues:
```bash
# Step 1: Fix basic type errors
npm run type-check

# Step 2: Fix linting errors
npm run lint -- --fix

# Step 3: Run strict check
npm run type-check:strict
```

## Best Practices

1. **Run type-check before every commit**
2. **Use strict mode for production code**
3. **Fix type errors immediately** - Don't let them accumulate
4. **Enable watch mode during development**
5. **Add type-check to CI/CD pipeline**
6. **Use explicit return types** - Helps catch errors early
7. **Avoid `any` type** - Use proper types or `unknown`
8. **Enable all strict flags in tsconfig.json** - For long-term maintainability

## MediChain AI Project Status

Current type safety: ✅ All pages building successfully

Run `npm run type-check:strict` to verify production readiness!
