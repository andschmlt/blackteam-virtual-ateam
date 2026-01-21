<?php
/**
 * PostHog + NavBoost Integration for metrotimes.com
 * PostHog Project ID: 295244
 * Site Type: News/Media
 * Generated: 2026-01-21
 */
if (!defined('ABSPATH')) exit;

function metrotimes_com_enqueue_posthog_scripts() {
    wp_enqueue_script('posthog-js', 'https://us-assets.i.posthog.com/static/array.js', array(), null, false);
    wp_add_inline_script('posthog-js', "
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split('.');2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement('script')).type='text/javascript',p.async=!0,p.src=s.api_host+'/static/array.js',(r=t.getElementsByTagName('script')[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a='posthog',u.people=u.people||[],u.toString=function(t){var e='posthog';return'posthog'!==a&&(e+='.'+a),t||(e+=' (stub)'),e},u.people.toString=function(){return u.toString(1)+'.people (stub)'},o='capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys'.split(' '),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
        posthog.init('phc_bac3vRylsrdbqYnOmVz9yAxCIlUSPWIRRAcs6qJ5OL5', {
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
    wp_enqueue_script('navboost-tracker', get_template_directory_uri() . '/js/navboost-tracker.js', array('posthog-js'), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'metrotimes_com_enqueue_posthog_scripts');

function metrotimes_com_add_body_class($classes) {
    if (is_front_page()) $classes[] = 'template-homepage';
    elseif (is_single()) $classes[] = 'template-article';
    elseif (is_category()) $classes[] = 'template-category';
    elseif (is_author()) $classes[] = 'template-author';
    elseif (is_tag()) $classes[] = 'template-tag';
    elseif (is_search()) $classes[] = 'template-search';
    elseif (is_page()) $classes[] = 'template-page';
    return $classes;
}
add_filter('body_class', 'metrotimes_com_add_body_class');

function metrotimes_com_track_article_meta() {
    if (!is_single()) return;
    global $post;
    $categories = wp_get_post_categories($post->ID, array('fields' => 'names'));
    $tags = wp_get_post_tags($post->ID, array('fields' => 'names'));
    $author = get_the_author();
    $word_count = str_word_count(strip_tags($post->post_content));
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
                'content_vertical': 'local_news'
            });
        }
    </script>
    <?php
}
add_action('wp_footer', 'metrotimes_com_track_article_meta');
