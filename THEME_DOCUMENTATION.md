# Theme System Documentation
## Light & Dark Mode Support

**Last Updated:** December 5, 2025  
**Version:** 2.0

---

## 📋 Overview

The Expense Tracker application now supports both **Light** and **Dark** themes with automatic detection and proper contrast for text visibility in both modes.

---

## 🎨 Theme Specifications

### Light Theme
| Element | Color | Hex Value | Usage |
|---------|-------|-----------|-------|
| **Background** | White | `#ffffff` | Main app background |
| **Secondary Background** | Light Gray | `#f3f4f6` | Input fields, cards |
| **Text** | Dark Gray | `#1f2937` | Main text content |
| **Primary Button** | Blue | `#0066cc` | Action buttons |
| **Primary Button Hover** | Darker Blue | `#0052a3` | Button hover state |
| **Error/Negative** | Red | `#dc3545` | Negative balance, warnings |
| **Error Background** | Light Red | `rgba(220, 53, 69, 0.1)` | Error message background |
| **Border** | Light Gray | `#d1d5db` | Input field borders |

### Dark Theme
| Element | Color | Hex Value | Usage |
|---------|-------|-----------|-------|
| **Background** | Almost Black | `#0e1117` | Main app background |
| **Secondary Background** | Dark Gray | `#21262d` | Input fields, cards |
| **Text** | Light Gray | `#e6edf3` | Main text content |
| **Primary Button** | Green | `#238636` | Action buttons |
| **Primary Button Hover** | Bright Green | `#2ea043` | Button hover state |
| **Error/Negative** | Bright Red | `#ff6b6b` | Negative balance, warnings |
| **Error Background** | Red Tint | `rgba(255, 107, 107, 0.1)` | Error message background |
| **Border** | Gray | `#30363d` | Input field borders |

---

## 🔄 How Theme Detection Works

The application automatically detects the current theme at startup:

```python
# From Loginmenu_updated.py (Lines 11-13)
try:
    theme = st.config.get_option("theme.base")
except:
    theme = "light"
```

The theme value is then used to apply the appropriate CSS styles to all elements.

---

## 🎛️ How Users Switch Themes

### Method 1: Streamlit Settings (Recommended)
1. Open the Expense Tracker app in your browser
2. Click the **⚙️ (Settings)** icon in the top-right corner
3. Select **Light theme** or **Dark theme**
4. The application will immediately update with the new colors

### Method 2: Browser Developer Tools (For Testing)
If you want to force a specific theme during development:

```javascript
// Open browser console (F12 or Ctrl+Shift+I)
// Force light theme
localStorage.setItem("theme", "light");
// Force dark theme
localStorage.setItem("theme", "dark");
// Then refresh the page
```

---

## 🎯 Key UI Elements & Their Styling

### 1. Login Title
- **Light**: Dark Gray text on white background
- **Dark**: Light Gray text on dark background
- **Font Size**: 2rem, Bold
- **Alignment**: Center

### 2. Buttons
- **Light**: Blue button with darker blue hover state
- **Dark**: Green button with brighter green hover state
- **Text**: Always white for contrast

### 3. Negative Balance Display
- **Light**: Red text on light red background
- **Dark**: Bright red text on dark red background
- **Always**: Indicates insufficient funds with visible warning

### 4. Input Fields
- **Light**: Light gray background with dark border
- **Dark**: Dark gray background with light border
- **Text**: Always readable (dark in light mode, light in dark mode)

### 5. Dataframes & Tables
- **Light**: White background with light gray rows
- **Dark**: Dark background with darker gray rows
- **Text**: Automatically adjusted for readability

---

## ✅ Accessibility Standards

The theme system ensures:

✅ **WCAG AA Compliance**
- Minimum contrast ratio of 4.5:1 for normal text
- Minimum contrast ratio of 3:1 for large text

✅ **Visual Consistency**
- All UI elements follow the same color scheme
- No jarring color transitions when switching themes

✅ **User Comfort**
- Dark theme reduces eye strain in low-light environments
- Light theme provides clear visibility in bright environments

---

## 📄 Configuration Files

### 1. `.streamlit/config.toml`
**Location**: `Streamlit_project/.streamlit/config.toml`

Controls:
- Default theme (light/dark)
- Primary colors
- Text colors
- Font preferences

### 2. CSS Styles in `Loginmenu_updated.py`
**Location**: Lines 11-73 (Light Theme) and conditional styling

Defines:
- Responsive styles for each theme
- Component-specific styling (buttons, inputs, etc.)
- Animation and hover effects

---

## 🔧 Customization Guide

### To Change Light Theme Colors

Edit `.streamlit/config.toml`:
```toml
[theme]
base = "light"
primaryColor = "#0066cc"        # Change button color
backgroundColor = "#ffffff"    # Change background
textColor = "#1f2937"          # Change text color
```

Edit `Loginmenu_updated.py` (Lines 55-74) for CSS overrides:
```python
.stButton button {
    background-color: #0066cc !important;  # Change here
    color: #ffffff !important;
}
```

### To Change Dark Theme Colors

Edit `Loginmenu_updated.py` (Lines 30-53):
```python
.stApp {
    background-color: #0e1117 !important;  # Change here
    color: #e6edf3 !important;             # Change here
}
```

---

## 🚀 Testing the Theme System

### Test Light Theme:
1. Open app with settings configured for Light theme
2. Verify all text is readable
3. Check button colors and hover states
4. Verify negative balance displays in red

### Test Dark Theme:
1. Switch to Dark theme in settings
2. Verify background is dark (#0e1117)
3. Verify all text is visible (light gray)
4. Check button colors change to green

### Test Theme Switching:
1. Open app in Light theme
2. Click Settings → Choose Dark theme
3. Verify immediate color update
4. Click Settings → Choose Light theme
5. Verify immediate revert to light colors

---

## 🐛 Troubleshooting

### Issue: Text is not visible
**Solution**: 
- Clear browser cache (Ctrl+Shift+Delete)
- Reload the page (Ctrl+R or F5)
- Check if theme is properly set in Settings

### Issue: Colors look wrong
**Solution**:
- Check `.streamlit/config.toml` for proper hex values
- Ensure CSS rules have `!important` flag for overrides
- Check browser developer console for CSS errors

### Issue: Theme doesn't change when settings are updated
**Solution**:
- Restart the Streamlit server: `streamlit run Loginmenu_updated.py`
- Clear browser cache and cookies
- Try a different browser

---

## 📊 Color Reference Chart

```
LIGHT THEME:
┌────────────────┬─────────────┬──────────┐
│ Element        │ Color       │ Hex      │
├────────────────┼─────────────┼──────────┤
│ Background     │ White       │ #ffffff  │
│ Text           │ Dark Gray   │ #1f2937  │
│ Button         │ Blue        │ #0066cc  │
│ Error          │ Red         │ #dc3545  │
└────────────────┴─────────────┴──────────┘

DARK THEME:
┌────────────────┬─────────────┬──────────┐
│ Element        │ Color       │ Hex      │
├────────────────┼─────────────┼──────────┤
│ Background     │ Dark        │ #0e1117  │
│ Text           │ Light Gray  │ #e6edf3  │
│ Button         │ Green       │ #238636  │
│ Error          │ Bright Red  │ #ff6b6b  │
└────────────────┴─────────────┴──────────┘
```

---

## 📝 Files Modified

| File | Changes | Purpose |
|------|---------|---------|
| `Loginmenu_updated.py` | Added theme detection and conditional CSS | Main styling logic |
| `.streamlit/config.toml` | Updated theme configuration | Default theme settings |
| `THEME_DOCUMENTATION.md` | New file | This documentation |

---

## 🎓 Best Practices

1. **Always Test Both Themes**: Before deployment, test your changes in both light and dark themes
2. **Use High Contrast**: Ensure text-to-background contrast ratio is at least 4.5:1
3. **Test on Real Devices**: Colors may appear different on different displays
4. **Document Color Changes**: Keep track of why color changes were made
5. **Consider Accessibility**: Always prioritize readability over aesthetics

---

## 📞 Support & Questions

For issues with the theme system:
1. Check this documentation
2. Review `.streamlit/config.toml` settings
3. Clear browser cache and reload
4. Check browser console for CSS errors (F12 → Console tab)
5. Restart Streamlit server

---

**Version History:**
- v2.0 (2025-12-05): Implemented full light/dark theme support
- v1.0 (2025-12-05): Initial theme styling
