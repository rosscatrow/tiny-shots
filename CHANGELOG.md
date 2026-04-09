# changelog

## v1.6.0

- restyle photo detail page as classic mac os system 7 alert dialog
- double-outline border (outer + inner) matching real system 7 alerts
- use authentic mac os bomb icon
- larger title font, metadata moved below photo
- proper rounded-rect buttons with default-button outline ring
- remove share button from photo page
- remove share button from gallery cards

## v1.5.0

- default home page to most recent roll instead of all photos (closes #25)
- sort roll tabs newest-first, move "all" tab to the right

## v1.4.0

- fix silent caption/emoji generation failures, add visible error logging (closes #22)
- shrink gallery cards from 500px to 300px with polaroid-style padding (closes #24)
- narrow site container from 780px to 520px for tighter desktop layout
- add subtle gray dither pattern to window background

## v1.3.0

- password-protect admin pages with sha-256 hashed gate (closes #18)
- optional password protection for individual rolls (closes #17)
- protected rolls show lock icon in gallery tab bar
- photos from locked rolls hidden from "all" view until unlocked
- inline password prompt styled in retro mac os aesthetic
- roll password management in manage.html (set/clear per roll)
- password field on new roll creation in upload.html
- fix emoji picker not working in roll password fields (closes #21)
- add admin link to gallery title bar (closes #23)
- session-based unlock via sessionstorage for both admin and roll gates
- new file: site-config.json for admin password hash

## v1.2.0

- add pixel-art camera favicon in classic mac os icon style (closes #19)
- favicon serves as svg for modern browsers, ico as fallback
- favicon links added to all html pages
- update readme to reflect current site architecture

## v1.1.0

- add rolls (album) feature for grouping photos
- add admin hub, upload page, and gallery management page
- auto-generate weird titles on upload via claude vision api
- per-photo title generation on manage page
- url hash-based roll filtering for shareable links
- auto-merge workflow for claude/* branches
- restyle admin pages to match mac os 9 aesthetic

## v1.0.0

- initial public gallery with classic mac os aesthetic
- single-column photo layout with hover effects
- dithered background, window chrome, noise overlay
- photo titles with emoji
- github pages deployment
