==================
 nti.recipes.json
==================

.. image:: https://travis-ci.org/NextThought/nti.recipes.json.svg?branch=master
    :target: https://travis-ci.org/NextThought/nti.recipes.json

.. image:: https://coveralls.io/repos/github/NextThought/nti.recipes.json/badge.svg?branch=master
    :target: https://coveralls.io/github/NextThought/nti.recipes.json?branch=master

This is a ``zc.buildout`` recipe that programatically creates JSON files

Lets look at an example using a buildout part::

  [nodeserver-env]
  recipe = nti.recipes.json
  output-file = /home/user/etc/nodeserver-env.json
  contents-section = nodeserver-env-root

  [nodeserver-env-root]
  stripe-section = nodeserver-stripe
  jquery-payment-section = nodeserver-jquery.payment

  [nodeserver-jquery.payment]
  requires =
    jquery
    stripe
    **end-list**
  url = https://my.server.com/libs/jquery.payment/1.3.2/jquery.payment.min.js
  definesSymbol = jQuery.payment

  [nodeserver-stripe]
  url = https://js.stripe.com/v2/
  definesSymbol = Stripe

  
The output for /home/user/etc/nodeserver-env.json will be::

	{
	    "jquery-payment": {
			"definesSymbol": "jQuery.payment",
			"requires": [
				"jquery",
				"stripe"
			],
			"url": "https://my.server.com/libs/jquery.payment/1.3.2/jquery.payment.min.js"
		},
		"stripe": {
			"definesSymbol": "Stripe",
			"url": "https://js.stripe.com/v2/"
		}
	}
