# Request Signature Access Button - Visual Guide

## 📸 Button Appearance

### Normal State
```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  AUTHORIZATION          [🔑 Request Signature Access]     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Hover State (Elevated)
```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  AUTHORIZATION          [🔑 Request Signature Access] ↑   │
│                         └─────────────────────────┘       │
│                              (shadow effect)               │
└────────────────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

### Button Colors
- **Background**: Purple gradient
  - Start: `#8b5cf6` (Violet 500)
  - End: `#7c3aed` (Violet 600)
- **Text**: White (`#ffffff`)
- **Icon**: White key icon
- **Shadow**: Purple with 20% opacity

### Hover Colors
- **Background**: Darker purple gradient
  - Start: `#7c3aed` (Violet 600)
  - End: `#6d28d9` (Violet 700)
- **Shadow**: Purple with 30% opacity (more prominent)

## 📐 Dimensions

```
┌─────────────────────────────────────┐
│  🔑  Request Signature Access       │  ← Height: ~36px
│                                     │
└─────────────────────────────────────┘
     ↑                               ↑
  Icon (16px)                  Text (14px)
  
  Total Width: Auto (fits content + padding)
  Padding: 8px 16px
  Border Radius: 6px
  Gap between icon and text: 8px
```

## 🖼️ Full Authorization Section Layout

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║  AUTHORIZATION              [🔑 Request Signature Access]    ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌─────────────┬─────────────┬─────────────┬─────────────┐  ║
║  │ PREPARED BY │ CHECKED BY  │ REVIEWED BY │ APPROVED BY │  ║
║  ├─────────────┼─────────────┼─────────────┼─────────────┤  ║
║  │             │             │             │             │  ║
║  │  [Sig Img]  │  [Sig Img]  │  [Sig Img]  │  [Sig Img]  │  ║
║  │             │             │             │             │  ║
║  ├─────────────┼─────────────┼─────────────┼─────────────┤  ║
║  │ O.M. LAVA   │ JMM MATA    │ EL ADIONG   │ C.C. AMIG.  │  ║
║  │ [e-sig btn] │ [e-sig btn] │ [e-sig btn] │ [e-sig btn] │  ║
║  ├─────────────┼─────────────┼─────────────┼─────────────┤  ║
║  │ Prin. Engr. │ Manager     │ Acting Mgr. │ Dept. Mgr.  │  ║
║  └─────────────┴─────────────┴─────────────┴─────────────┘  ║
║                                                               ║
║  ┌─────────────┬─────────────┬─────────────┬─────────────┐  ║
║  │ PREPARED BY │ CHECKED BY  │ REVIEWED BY │ APPROVED BY │  ║
║  ├─────────────┼─────────────┼─────────────┼─────────────┤  ║
║  │             │             │             │             │  ║
║  │  [Sig Img]  │  [Sig Img]  │  [Sig Img]  │  [Sig Img]  │  ║
║  │             │             │             │             │  ║
║  ├─────────────┼─────────────┼─────────────┼─────────────┤  ║
║  │ D.R.B CAIRO │ JMM MATA    │ EL ADIONG   │ DB ESMADE   │  ║
║  │ [e-sig btn] │ [e-sig btn] │ [e-sig btn] │ [e-sig btn] │  ║
║  ├─────────────┼─────────────┼─────────────┼─────────────┤  ║
║  │ Prin. Engr. │ Manager     │ OIC-Dept.   │ Acting Dept.│  ║
║  └─────────────┴─────────────┴─────────────┴─────────────┘  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

## 🎬 Animation Sequence

### On Hover
```
Frame 1 (0ms):     [🔑 Request Signature Access]
                   └─────────────────────────┘
                   
Frame 2 (150ms):   [🔑 Request Signature Access] ↑
                   └─────────────────────────┘
                        (lifts 2px up)
                        
Frame 3 (300ms):   [🔑 Request Signature Access] ↑
                   └─────────────────────────┘
                     (shadow expands)
```

### On Click
```
Frame 1:           [🔑 Request Signature Access] ↑
                   └─────────────────────────┘
                   
Frame 2:           [🔑 Request Signature Access]
                   └─────────────────────────┘
                        (presses down)
                        
Frame 3:           → Navigate to /request-signature-access
```

## 💡 Usage Context

### When to Use
- ✅ User needs to request access for a signatory
- ✅ User doesn't have authorization to add e-signatures
- ✅ User wants to enable e-signature for a specific person
- ✅ Quick access from report preview

### What Happens
1. **Click button** → Navigate to Request Signature Access page
2. **Select signatory** → Choose from dropdown
3. **Fill justification** → Explain why access is needed
4. **Submit request** → Auto-processor handles it
5. **Receive email** → Get signature setup link
6. **Setup signature** → Draw and save
7. **Use in reports** → Add e-signatures to reports

## 🎯 Design Rationale

### Why Purple?
- **Distinct**: Stands out from blue e-signature buttons
- **Professional**: Purple conveys authority and trust
- **Accessible**: Good contrast with white text
- **Modern**: Gradient gives contemporary feel

### Why Key Icon?
- **Symbolic**: Represents access/authorization
- **Recognizable**: Universal symbol for permissions
- **Clear**: Immediately conveys purpose
- **Consistent**: Matches security theme

### Why This Position?
- **Visible**: Top of Authorization section
- **Logical**: Related to signatures
- **Accessible**: Easy to find and click
- **Non-intrusive**: Doesn't interfere with signature table

## ✅ Accessibility

- **Keyboard**: Can be focused and activated with Enter/Space
- **Screen Readers**: Has descriptive title attribute
- **Color Contrast**: Meets WCAG AA standards (white on purple)
- **Focus Indicator**: Visible outline when focused
- **Touch Target**: Large enough for mobile (44x44px minimum)

## 📱 Responsive Behavior

### Desktop (>1024px)
```
AUTHORIZATION              [🔑 Request Signature Access]
```

### Tablet (768px - 1024px)
```
AUTHORIZATION         [🔑 Request Access]
```

### Mobile (<768px)
```
AUTHORIZATION
[🔑 Request Access]
```

## 🎨 Integration with Existing UI

The button seamlessly integrates with:
- ✅ Existing color scheme
- ✅ Button styling patterns
- ✅ Animation standards
- ✅ Spacing guidelines
- ✅ Typography system
- ✅ Icon library (PrimeIcons)

## 🚀 Ready to Use!

The button is now live and ready for users to request signature access directly from the report preview!
