<?php
/**
 * PostHog + NavBoost Integration for europeangaming.eu
 *
 * Add this code to your theme's functions.php file
 * OR create a custom plugin with this code
 *
 * PostHog Project ID: 290042
 * Site Type: News/Media (iGaming Industry)
 *
 * @version 1.0.0
 * @date 2026-01-21
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Enqueue PostHog and NavBoost scripts
 */
function europeangaming_enqueue_posthog_scripts() {
    // PostHog base snippet (loads from CDN)
    wp_enqueue_script(
        'posthog-js',
        'https://us-assets.i.posthog.com/static/array.js',
        array(),
        null,
        false // Load in header
    );

    // PostHog initialization
    wp_add_inline_script('posthog-js', "
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split('.');2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement('script')).type='text/javascript',p.async=!0,p.src=s.api_host+'/static/array.js',(r=t.getElementsByTagName('script')[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a='posthog',u.people=u.people||[],u.toString=function(t){var e='posthog';return'posthog'!==a&&(e+='.'+a),t||(e+=' (stub)'),e},u.people.toString=function(){return u.toString(1)+'.people (stub)'},o='capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys'.split(' '),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

        posthog.init('phc_yL0Kmph4HtqQpW47JtiDnbowvmbMqVVZ0eVU4ayuFmx', {
            api_host: 'https://us.i.posthog.com',
            person_profiles: 'identified_only',
            // Page & Session Tracking
            capture_pageview: true,
            capture_pageleave: true,
            // Autocapture (clicks, forms, inputs)
            autocapture: true,
            // Core Web Vitals (LCP, CLS, INP)
            autocapture_web_vitals_opt_in: true,
            // Performance metrics
            capture_performance_opt_in: true,
            // Session Recording
            session_recording: {
                maskAllInputs: true,
                maskTextContent: false
            },
            // Heatmaps
            enable_heatmaps: true,
            // Console logs (for debugging)
            capture_console_log_opt_in: false
        });
    ", 'before');

    // NavBoost tracker (load after PostHog)
    wp_enqueue_script(
        'navboost-tracker',
        get_template_directory_uri() . '/js/navboost-tracker.js',
        array('posthog-js'),
        '1.0.0',
        true // Load in footer
    );
}
add_action('wp_enqueue_scripts', 'europeangaming_enqueue_posthog_scripts');

/**
 * Add page template data attribute for NavBoost
 */
function europeangaming_add_body_class($classes) {
    // Add template type for NavBoost detection
    if (is_front_page()) {
        $classes[] = 'template-homepage';
    } elseif (is_single()) {
        $classes[] = 'template-article';

        // Check for press releases
        if (has_category('press-release') || has_tag('press-release')) {
            $classes[] = 'template-press-release';
        }
    } elseif (is_category()) {
        $classes[] = 'template-category';
    } elseif (is_author()) {
        $classes[] = 'template-author';
    } elseif (is_tag()) {
        $classes[] = 'template-tag';
    } elseif (is_search()) {
        $classes[] = 'template-search';
    } elseif (is_page()) {
        $classes[] = 'template-page';

        // Check for events page
        if (is_page('events') || is_page('conferences')) {
            $classes[] = 'template-events';
        }
    }

    return $classes;
}
add_filter('body_class', 'europeangaming_add_body_class');

/**
 * Add data attributes to CTAs for better tracking
 */
function europeangaming_add_cta_attributes($content) {
    // Add data-cta-type to common CTA patterns
    $patterns = array(
        // Newsletter forms
        '/<form([^>]*)(newsletter|subscribe)([^>]*)>/i' => '<form$1$2$3 data-cta-type="newsletter">',
        // Read more links
        '/<a([^>]*class="[^"]*read-more[^"]*"[^>]*)>/i' => '<a$1 data-cta-type="read-more">',
        // Share buttons
        '/<a([^>]*class="[^"]*share[^"]*"[^>]*)>/i' => '<a$1 data-cta-type="social-share">',
        // Event links
        '/<a([^>]*)(ice365|sigma|gaming|conference)([^>]*)>/i' => '<a$1$2$3 data-cta-type="event">',
    );

    foreach ($patterns as $pattern => $replacement) {
        $content = preg_replace($pattern, $replacement, $content);
    }

    return $content;
}
add_filter('the_content', 'europeangaming_add_cta_attributes');

/**
 * Track article metadata for better analytics
 */
function europeangaming_track_article_meta() {
    if (!is_single()) {
        return;
    }

    global $post;

    $categories = wp_get_post_categories($post->ID, array('fields' => 'names'));
    $tags = wp_get_post_tags($post->ID, array('fields' => 'names'));
    $author = get_the_author();
    $word_count = str_word_count(strip_tags($post->post_content));

    // iGaming specific: Check if it's a press release
    $is_press_release = has_category('press-release') || has_tag('press-release');

    ?>
    <script>
        if (typeof posthog !== 'undefined') {
            posthog.register({
                'article_id': <?php echo $post->ID; ?>,
                'article_title': <?php echo json_encode($post->post_title); ?>,
                'article_categories': <?php echo json_encode($categories); ?>,
                'article_tags': <?php echo json_encode($tags); ?>,
                'article_author': <?php echo json_encode($author); ?>,
                'article_word_count': <?php echo $word_count; ?>,
                'article_publish_date': <?php echo json_encode(get_the_date('Y-m-d')); ?>,
                'is_press_release': <?php echo $is_press_release ? 'true' : 'false'; ?>,
                'content_vertical': 'igaming'
            });
        }
    </script>
    <?php
}
add_action('wp_footer', 'europeangaming_track_article_meta');
