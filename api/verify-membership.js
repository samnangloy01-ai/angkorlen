const Stripe = require('stripe');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const sessionId = req.query && req.query.session_id;

  if (!sessionId || !sessionId.startsWith('cs_')) {
    return res.status(400).json({ error: 'Missing or invalid checkout session.' });
  }

  try {
    const stripe = Stripe(process.env.STRIPE_SECRET_KEY);

    const session = await stripe.checkout.sessions.retrieve(sessionId, {
      expand: ['subscription']
    });

    const subscription = session.subscription;

    const active =
      session.mode === 'subscription' &&
      (session.payment_status === 'paid' ||
        session.payment_status === 'no_payment_required') &&
      subscription &&
      ['active', 'trialing'].includes(subscription.status);

    return res.status(200).json({
      active: Boolean(active),
      plan: session.metadata?.plan || null,
      subscription_status: subscription?.status || null
    });
  } catch (error) {
    console.error('Stripe membership verification error:', error);

    return res.status(400).json({
      active: false,
      error: 'Membership could not be verified.'
    });
  }
};
