<?php
/**
 * PostHog Full Tracking - philadelphiaweekly.com
 *
 * Includes:
 * - PostHog SDK
 * - NavBoost Tracker
 * - Enhanced Conversion Tracker (5 conversion types)
 *
 * DEPLOYMENT:
 * 1. Add this code to your theme's functions.php
 * 2. OR create a custom plugin with this code
 * 3. OR use a code snippets plugin
 *
 * PostHog Project ID: 295222
 * Generated: 2026-01-21
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Enqueue PostHog tracking scripts
 */
function philadelphiaweekly_com_posthog_tracking() {
    ?>
    <!-- PostHog SDK -->
    <script>
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

        posthog.init('phc_7Uz92UNP9iMQMXQ1FncqvmhH0NCHPuei5KLeJb6ZekU', {
            api_host: 'https://us.i.posthog.com',
            capture_pageview: true,
            capture_pageleave: true,
            autocapture: true,
            persistence: 'localStorage+cookie',
            loaded: function(posthog) {
                console.log('[PostHog] Loaded for philadelphiaweekly.com');
            }
        });
    </script>

    <!-- NavBoost Tracker -->
    <script>
    <?php echo file_get_contents(dirname(__FILE__) . '/navboost-tracker.js'); ?>
    </script>

    <!-- Enhanced Conversion Tracker -->
    <script>
    <?php echo file_get_contents(dirname(__FILE__) . '/conversion-tracker.js'); ?>
    </script>
    <?php
}
add_action('wp_head', 'philadelphiaweekly_com_posthog_tracking', 1);

/**
 * Alternative: Load scripts as external files (better caching)
 * Uncomment this and comment out the above function if preferred
 */
/*
function philadelphiaweekly_com_posthog_tracking_external() {
    // PostHog SDK
    wp_enqueue_script(
        'posthog-sdk',
        'https://us.i.posthog.com/static/array.js',
        array(),
        null,
        false
    );

    // Initialize PostHog
    wp_add_inline_script('posthog-sdk', "
        posthog.init('phc_7Uz92UNP9iMQMXQ1FncqvmhH0NCHPuei5KLeJb6ZekU', {
            api_host: 'https://us.i.posthog.com',
            capture_pageview: true,
            capture_pageleave: true,
            autocapture: true
        });
    ");

    // NavBoost + Conversion trackers
    wp_enqueue_script(
        'navboost-tracker',
        get_template_directory_uri() . '/js/navboost-tracker.js',
        array('posthog-sdk'),
        '1.0.0',
        true
    );

    wp_enqueue_script(
        'conversion-tracker',
        get_template_directory_uri() . '/js/conversion-tracker.js',
        array('posthog-sdk', 'navboost-tracker'),
        '1.0.0',
        true
    );
}
add_action('wp_enqueue_scripts', 'philadelphiaweekly_com_posthog_tracking_external');
*/

/**
 * Add custom conversion tracking for WooCommerce (if applicable)
 */
function philadelphiaweekly_com_woocommerce_conversions() {
    if (!class_exists('WooCommerce')) return;
    ?>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Track add to cart
        jQuery(document.body).on('added_to_cart', function(e, fragments, cart_hash, button) {
            if (typeof posthog !== 'undefined') {
                posthog.capture('conversion:add_to_cart', {
                    product_id: button.data('product_id'),
                    value: 2
                });
            }
        });
    });
    </script>
    <?php
}
add_action('wp_footer', 'philadelphiaweekly_com_woocommerce_conversions');

/**
 * Track comment submissions as conversions
 */
function philadelphiaweekly_com_comment_conversion($comment_id, $comment_approved) {
    if ($comment_approved) {
        ?>
        <script>
        if (typeof posthog !== 'undefined') {
            posthog.capture('conversion:comment_submit', {
                conversion_type: 'comment',
                comment_id: <?php echo $comment_id; ?>,
                value: 1
            });
        }
        </script>
        <?php
    }
}
add_action('comment_post', 'philadelphiaweekly_com_comment_conversion', 10, 2);

/**
 * Track search queries
 */
function philadelphiaweekly_com_search_tracking() {
    if (is_search()) {
        $search_query = get_search_query();
        ?>
        <script>
        if (typeof posthog !== 'undefined') {
            posthog.capture('site_search', {
                search_query: '<?php echo esc_js($search_query); ?>',
                results_count: <?php echo $GLOBALS['wp_query']->found_posts; ?>
            });
        }
        </script>
        <?php
    }
}
add_action('wp_footer', 'philadelphiaweekly_com_search_tracking');
