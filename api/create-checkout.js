const Stripe = require('stripe');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const stripe = Stripe(process.env.STRIPE_SECRET_KEY);
    const { plan } = req.body || {};

    const priceId =
      plan === 'monthly'
        ? process.env.STRIPE_PRICE_MONTHLY
        : plan === 'yearly'
          ? process.env.STRIPE_PRICE_YEARLY
          : null;

    if (!priceId) {
      return res.status(400).json({ error: 'Invalid membership plan.' });
    }

    const forwardedProto = req.headers['x-forwarded-proto'] || 'https';
    const host = req.headers.host;
    const siteUrl = (process.env.SITE_URL || `${forwardedProto}://${host}`).replace(/\/$/, '');

    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [
        {
          price: priceId,
          quantity: 1
        }
      ],
      success_url: `${siteUrl}/?membership=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${siteUrl}/?membership=cancelled`,
      allow_promotion_codes: false
    });

    return res.status(200).json({ url: session.url });
  } catch (error) {
    console.error('Stripe checkout error:', error);
    return res.status(500).json({ error: 'Unable to create checkout session.' });
  }
};
