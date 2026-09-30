# AngkorLens Stripe + Vercel

This build connects the AngkorLens membership buttons to Stripe Checkout.

## Files

- `index.html` — existing AngkorLens site with the membership UI wired to `/api/create-checkout`
- `api/create-checkout.js` — creates a hosted Stripe subscription Checkout Session
- `api/verify-membership.js` — verifies a completed subscription before unlocking the photo lightbox
- `api/stripe-webhook.js` — starter webhook endpoint for future persistent membership records
- `package.json` — Stripe server SDK dependency
- `.env.example` — names of the Vercel environment variables

## Important

The Stripe secret key must stay in Vercel Environment Variables and must never be committed to GitHub.

This first version gates the browser lightbox after server-side Stripe verification. The original image files are still public if they remain on GitHub/raw URLs. For true protection of original-resolution files, move originals to private storage and have an authenticated server endpoint issue short-lived access URLs.
