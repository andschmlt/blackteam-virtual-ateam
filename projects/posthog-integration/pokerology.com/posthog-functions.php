<?php
/**
 * PostHog Analytics Integration for pokerology.com
 *
 * Setup Date: 2026-01-20
 * Project ID: 294549
 * Domain: pokerology.com
 * Site Type: Affiliate/Casino (Poker)
 *
 * INSTALLATION:
 * Add this code to your theme's functions.php file
 * or create a custom plugin.
 *
 * BlackTeam Project: BT-2026-002 (PostHog Analytics Platform Migration)
 */

/**
 * PostHog Analytics - Base Tracking
 * Loads PostHog SDK and initializes with project settings
 */
function pokerology_posthog_analytics() {
    ?>
    <script>
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

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
    </script>
    <?php
}
add_action('wp_head', 'pokerology_posthog_analytics', 2);

/**
 * NavBoost Tracking Module
 * Loads the NavBoost tracker for engagement metrics
 */
function pokerology_navboost_tracker() {
    wp_enqueue_script(
        'navboost-tracker',
        get_stylesheet_directory_uri() . '/js/navboost-tracker.js',
        array(),
        '1.0.0',
        true
    );
}
add_action('wp_enqueue_scripts', 'pokerology_navboost_tracker', 20);
