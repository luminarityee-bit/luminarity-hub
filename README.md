# LUMINARITY HUB

Internal tool για συνεργάτες — login + dashboards + ΕΦΑΡΜΟΓΗ ΔΕΗ.

## Deployment σε GitHub Pages (δωρεάν)

### 1. Δημιουργία repo
1. Πήγαινε στο https://github.com/new
2. Owner: ο λογαριασμός σου · Name: `luminarity-hub` (ή άλλο)
3. **Public** (το δωρεάν Pages δουλεύει μόνο σε public repos)
4. Initialize με README → ΟΧΙ (έχουμε δικό μας)
5. Create

### 2. Upload φακέλου
**Επιλογή Α — Drag & drop (απλή):**
1. Στο repo: «Add file» → «Upload files»
2. Σύρε ΟΛΟ τον φάκελο `LUMINARITY_HUB/` (όλα τα περιεχόμενα — όχι τον ίδιο τον φάκελο)
3. Commit

**Επιλογή Β — Git CLI:**
```bash
cd "C:/Users/ΝΙΚΗΦΟΡΟΣ/OneDrive - LUMINARITY/Επιφάνεια εργασίας/LUMINARITY_HUB"
git init
git add .
git commit -m "Initial upload"
git branch -M main
git remote add origin https://github.com/<USERNAME>/luminarity-hub.git
git push -u origin main
```

### 3. Enable GitHub Pages
1. Στο repo: Settings → Pages
2. Source: «Deploy from a branch»
3. Branch: `main` · folder: `/ (root)`
4. Save
5. Σε ~1 λεπτό θα δεις: «Your site is live at `https://<USERNAME>.github.io/luminarity-hub/`»

### 4. Δοκιμή
- Άνοιξε `https://<USERNAME>.github.io/luminarity-hub/hub.html`
- Login με `LUMI0000` (admin) ή `BO1234` (back office)
- Όλα πρέπει να δουλεύουν, συμπεριλαμβανομένου του ΕΦΑΡΜΟΓΗ μέσα σε iframe

## Profiles ανά συνεργάτη

Άλλαξε στο `hub.html`, πάνω-πάνω στο `<script>` block:

```js
const USERS = {
  'LUMI0000':   {role:'admin',      name:'Admin'},
  'GIANNIS_42': {role:'backoffice', name:'Γιάννης'},
  'MARIA_99':   {role:'backoffice', name:'Μαρία'},
  // ...
};
```

Push στο GitHub → αυτόματη ενημέρωση του Pages μετά από ~1 λεπτό.

## Ενημέρωση όρων ΔΕΗ

1. Αντικατέστησε τα PDFs στον φάκελο `αιτησεις/` (ίδια ονόματα)
2. Διπλό click στο `Ενημέρωση Όρων.bat` — ενημερώνει τοπικά το `fillContract.html`
3. `git add ΕΦΑΡΜΟΓΗ/fillContract.html && git commit -m "Update terms" && git push`
4. Σε ~1 λεπτό όλοι οι συνεργάτες παίρνουν τους νέους όρους

## Σημειώσεις ασφάλειας

⚠️ **Public repo**: οι κωδικοί στο `USERS` map είναι ορατοί σε όποιον ανοίγει το source. Για παραγωγή χρειάζεται **private repo + GitHub Pro** ή proper backend (Apps Script). Για αρχικό testing είναι ΟΚ.
