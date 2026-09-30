const Stripe = require('stripe');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    if (!process.env.STRIPE_SECRET_KEY) {
      return res.status(500).json({ error: 'Stripe is not configured: STRIPE_SECRET_KEY is missing.' });
    }

    const { plan } = req.body || {};

    const priceId =
      plan === 'monthly'
        ? process.env.STRIPE_PRICE_MONTHLY
        : plan === 'yearly'
          ? process.env.STRIPE_PRICE_YEARLY
          : null;

    if (!priceId) {
      return res.status(500).json({
        error: plan === 'monthly'
          ? 'Stripe is not configured: STRIPE_PRICE_MONTHLY is missing.'
          : plan === 'yearly'
            ? 'Stripe is not configured: STRIPE_PRICE_YEARLY is missing.'
            : 'Invalid membership plan.'
      });
    }

    const stripe = Stripe(process.env.STRIPE_SECRET_KEY);

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
      metadata: {
        plan
      },
      subscription_data: {
        metadata: {
          plan
        }
      },
      success_url: `${siteUrl}/?membership=success&session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${siteUrl}/?membership=cancelled`,
      allow_promotion_codes: false
    });

    return res.status(200).json({ url: session.url });
  } catch (error) {
    console.error('Stripe checkout error:', error);
    return res.status(500).json({
      error: error?.message || 'Unable to create checkout session.'
    });
  }
};
