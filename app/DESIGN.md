---
name: Precision Fiscal
colors:
  surface: '#121414'
  surface-dim: '#121414'
  surface-bright: '#393939'
  surface-container-lowest: '#0d0e0f'
  surface-container-low: '#1b1c1c'
  surface-container: '#1f2020'
  surface-container-high: '#292a2a'
  surface-container-highest: '#343535'
  on-surface: '#e3e2e2'
  on-surface-variant: '#c6c6c6'
  inverse-surface: '#e3e2e2'
  inverse-on-surface: '#303031'
  outline: '#919191'
  outline-variant: '#474747'
  surface-tint: '#b0c6ff'
  primary: '#b0c6ff'
  on-primary: '#002d6f'
  primary-container: '#1a438f'
  on-primary-container: '#d9e2ff'
  inverse-primary: '#375ca8'
  secondary: '#bfc6dc'
  on-secondary: '#293041'
  secondary-container: '#3f4759'
  on-secondary-container: '#dbe2f9'
  tertiary: '#e0bbde'
  on-tertiary: '#412742'
  tertiary-container: '#593d5a'
  on-tertiary-container: '#fed7fa'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d9e2ff'
  primary-fixed-dim: '#b0c6ff'
  on-primary-fixed: '#001945'
  on-primary-fixed-variant: '#1a438f'
  secondary-fixed: '#dbe2f9'
  secondary-fixed-dim: '#bfc6dc'
  on-secondary-fixed: '#141b2c'
  on-secondary-fixed-variant: '#3f4759'
  tertiary-fixed: '#fed7fa'
  tertiary-fixed-dim: '#e0bbde'
  on-tertiary-fixed: '#2a122c'
  on-tertiary-fixed-variant: '#593d5a'
  background: '#121414'
  on-background: '#e3e2e2'
  surface-variant: '#343535'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  title-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  mono-data:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 48px
  container-max: 1440px
  gutter: 24px
---

## Brand & Style

This design system is engineered for high-stakes financial environments where clarity, speed of cognition, and professional trust are paramount. The brand personality is authoritative yet accessible—a "reliable advisor" aesthetic that minimizes cognitive load through a **Modern Corporate/Minimalist** approach, now optimized for a high-focus **Dark Mode** environment.

The design prioritizes information density without clutter. By utilizing a **rainbow** color variant, the system introduces a broader, more sophisticated spectrum of tonal accents into its professional foundation, ensuring that data trends and interactive elements are immediately distinguishable. The emotional response should be one of calm control; users should feel that their data is organized, secure, and dynamically actionable in a premium, low-strain interface.

## Colors

The palette is anchored by a **Muted Steel Blue** primary color, optimized for legibility and reduced eye strain within a dark interface while maintaining a professional SaaS aesthetic.

- **Primary (Steel Blue):** Used for navigation, active states, and core brand identifiers. It represents technical proficiency and stability.
- **Secondary (Slate Gray):** Used for supportive interactive elements and secondary actions, providing a balanced, low-vibrancy companion to the primary blue.
- **Tertiary (Dusty Plum):** Reserved for specialized data categories and alternative status indicators, adding sophisticated tonal variety to fiscal visualizations.
- **Neutrals:** A balanced range of **Neutral Grays** handles borders, secondary text, and background layering, ensuring high contrast for readability without being harsh.

## Typography

The system utilizes **Inter** for its exceptional legibility in data-heavy interfaces. Its tall x-height and clean apertures ensure that even small labels remain readable against dark backgrounds. 

For financial figures within data tables, a secondary monospace font (**JetBrains Mono**) is used to ensure tabular lining; this allows users to scan columns of numbers quickly as decimals and digits align vertically. 

Use `label-caps` for table headers and section overviews to create a clear structural hierarchy. `display-lg` is reserved for total balance views or hero dashboard metrics.

## Layout & Spacing

This design system employs a **12-column fluid grid** with a maximum container width of 1440px. The spacing scale is built on a 4px baseline, ensuring all components align to a predictable rhythm.

- **Desktop:** 24px margins and 24px gutters. Content should be grouped into cards that span 3, 4, 6, or 12 columns.
- **Tablet:** 16px margins and 16px gutters. Sidebar navigation collapses into a thin icon bar.
- **Mobile:** 16px margins. Layout reflows to a single column. Horizontal scrolling is permitted only for wide data tables to preserve data integrity.

Use `lg` (24px) padding for all internal card containers to maintain the "spacious" Enterprise SaaS feel.

## Elevation & Depth

To maintain a professional and flat aesthetic in dark mode, depth is communicated through **Tonal Layering** and **Low-Contrast Outlines** rather than traditional shadows, which can appear muddy on dark surfaces.

- **Level 0 (Background):** The darkest surface, used for the main application backdrop.
- **Level 1 (Cards/Surface):** Slightly lighter gray surfaces with a 1px solid border derived from the neutral palette to define boundaries.
- **Level 2 (Dropdowns/Modals):** Lighter tonal surfaces with a subtle, ultra-diffused glow or ambient shadow to indicate temporary interaction and focus.
- **Active State:** Elements being dragged or clicked use a 2px primary-colored border to indicate focus and separation from the background.

## Shapes

The shape language is **Soft** and restrained. A 0.25rem (4px) base radius is applied to standard buttons, input fields, and small UI widgets. Large containers and cards utilize 0.5rem (8px). 

This subtle rounding removes the "sharpness" of pure brutalism while maintaining a serious, geometric profile appropriate for financial services. Circular shapes are reserved strictly for user avatars and status indicators (pills).

## Components

### Buttons
- **Primary:** Solid Steel Blue (#5275C3) with high-contrast text.
- **Secondary:** Transparent background with a 1px Slate Gray border and Primary text.
- **Danger:** Solid muted red for destructive actions.

### Data Tables
- Use `label-caps` for headers.
- Row height: 52px for standard density.
- Use subtle tonal shifts on hover states to highlight rows.

### Stats Cards
- Prominent `headline-md` for the main metric.
- A small sparkline chart or percentage pill in the top right.
- Status-specific colors for positive and negative deltas, ensuring sufficient contrast against dark surfaces.

### Progress Bars
- 8px height with a fully rounded (pill) track.
- Background track color: Dark neutral surface container.
- Fill color: Use Primary Blue for standard progress, Tertiary Plum for special metrics, and Red for over-limit status.

### Modal Dialogs
- Centered on screen with a backdrop blur (4px) and semi-transparent dark overlay.
- Max width of 560px for standard inputs.
- Header must include a clear Title and a "Close" icon.

### Input Fields
- 1px neutral border with 8px horizontal padding.
- Focused state: 1px border becomes Primary Blue (#5275C3) with a subtle 2px glow of the same color at 15% opacity to stand out against the dark background.