/**
 * NavBoost Tracker v1.3.0 - Smart CTA Detection
 * Site Type: Universal (adaptable per site)
 * PostHog Integration
 * Generated: 2026-02-04
 *
 * CHANGELOG v1.3.0 (SMART CTA DETECTION):
 * - NEW: 3-Tier CTA Identification System
 *   - Tier 1: Explicit HTML attributes (data-cta-id, data-cta-name, id)
 *   - Tier 2: URL pattern derivation (/go/, /out/, /aff/, affiliate domains)
 *   - Tier 3: Position + element fingerprint (fallback)
 * - NEW: cta_id_tier property (1, 2, or 3)
 * - NEW: cta_id_method property (specific method used)
 * - NEW: cta_region property (header, footer, sidebar, article, etc.)
 * - NEW: cta_position property (nth position in region)
 * - NEW: cta_href_pattern property (detected URL pattern type)
 * - NEW: Diagnostic mode for CTA detection analysis
 * - ENHANCED: Consistent CTA IDs across sessions (no more random suffixes)
 *
 * INCLUDES v1.2.1 FIXES:
 * - CTA Template system with site-specific selectors
 * - Click handler error logging
 * - Individual selector testing
 *
 * INCLUDES v1.1.2 FIXES:
 * - Heartbeat events every 30s
 * - visibilitychange/pagehide handlers for mobile session capture
 *
 * Reference: NAVBOOST_v1.3.0_SPEC.md
 */

(function() {
    'use strict';

    var VERSION = '1.3.0';

    // ==========================================
    // CRITICAL: Always-on error logging
    // ==========================================
    function logError(context, error) {
        console.error('[NavBoost v' + VERSION + ' ERROR]', context, error);
        try {
            if (typeof posthog !== 'undefined') {
                posthog.capture('navboost:tracker_error', {
                    error_context: context,
                    error_message: error ? error.message : 'Unknown error',
                    error_stack: error ? error.stack : null,
                    tracker_version: VERSION,
                    page_url: window.location.href,
                    user_agent: navigator.userAgent
                });
            }
        } catch (e) {
            console.error('[NavBoost] Failed to send error telemetry:', e);
        }
    }

    function logInit(context) {
        console.log('[NavBoost v' + VERSION + ']', context);
    }

    function log() {
        if (CONFIG.DEBUG) {
            var args = ['[NavBoost v' + VERSION + ']'];
            for (var i = 0; i < arguments.length; i++) {
                args.push(arguments[i]);
            }
            console.log.apply(console, args);
        }
    }

    // ==========================================
    // CONFIGURATION
    // ==========================================
    var CONFIG = {
        SITE_DOMAIN: window.location.hostname,
        SITE_TYPE: 'Universal',
        VERTICAL: 'general',
        POSTHOG_PROJECT_ID: null, // Set per deployment

        // Heartbeat configuration
        HEARTBEAT_INTERVAL_MS: 30000,

        // Pogo detection threshold
        POGO_THRESHOLD_MS: 8000,

        // Scroll milestones
        SCROLL_MILESTONES: [25, 50, 75, 100],
        SCROLL_ZONES: {
            25: 'above_fold',
            50: 'cta_zone',
            75: 'content',
            100: 'footer'
        },

        // Google domains
        GOOGLE_DOMAINS: [
            'google.com', 'google.co.uk', 'google.de', 'google.fr', 'google.es',
            'google.it', 'google.nl', 'google.com.au', 'google.ca', 'google.co.in',
            'google.com.br', 'google.co.jp', 'google.ru', 'google.pl', 'google.se',
            'google.at', 'google.ch', 'google.be'
        ],

        // Dwell time benchmarks (News/Media)
        DWELL_BENCHMARKS: {
            VERY_BAD: 10000,
            WEAK: 30000,
            NORMAL: 60000,
            STRONG: 60001
        },

        // Vertical-specific targets
        TARGETS: {
            POGO_RATE: 20,
            DWELL_TIME: 60,
            CTA_CTR: 3,
            ENGAGEMENT_SCORE: 65,
            GOOD_ABANDONMENT: 10
        },

        // v1.3.0: CTA Selectors (customize per site)
        CTA_SELECTORS: [
            // Explicit CTA markers
            '[data-cta-id]',
            '[data-cta-name]',

            // Affiliate Promo Boxes
            '.pm-promo-code-container',
            '.pm-play-now',
            '.pm-play-now-link',
            '.pm-review',

            // Affiliate Links (rel patterns)
            'a[rel="nofollow noreferrer"]',
            'a[rel="nofollow noopener"]',
            'a[rel*="sponsored"]',

            // Common CTA classes
            '.cta-button',
            '.cta-link',
            '.btn-cta',
            '.affiliate-link',

            // GAMURS Blocks
            '.wp-block-gamurs-icon',
            '.wp-block-gamurs-article-tile__link',

            // Social sharing (URL patterns)
            'a[href*="twitter.com/intent"]',
            'a[href*="x.com/intent"]',
            'a[href*="facebook.com/sharer"]',
            'a[href*="reddit.com/submit"]',
            'a[href*="linkedin.com/share"]',

            // Outbound tracking patterns
            'a[href*="/go/"]',
            'a[href*="/out/"]',
            'a[href*="/aff/"]',
            'a[href*="/partner/"]'
        ],

        // v1.3.0: URL patterns for Tier 2 detection
        AFFILIATE_URL_PATTERNS: [
            { pattern: /\/go\/([a-zA-Z0-9_-]+)/i, prefix: 'affiliate', capture: 1 },
            { pattern: /\/out\/([a-zA-Z0-9_-]+)/i, prefix: 'outbound', capture: 1 },
            { pattern: /\/aff\/([a-zA-Z0-9_-]+)/i, prefix: 'affiliate', capture: 1 },
            { pattern: /\/partner\/([a-zA-Z0-9_-]+)/i, prefix: 'partner', capture: 1 },
            { pattern: /[?&]ref=([a-zA-Z0-9_-]+)/i, prefix: 'referral', capture: 1 },
            { pattern: /[?&]aff=([a-zA-Z0-9_-]+)/i, prefix: 'affiliate', capture: 1 },
            { pattern: /[?&]partner=([a-zA-Z0-9_-]+)/i, prefix: 'partner', capture: 1 }
        ],

        // v1.3.0: Known affiliate domains
        KNOWN_AFFILIATE_DOMAINS: [
            'betonlineaffiliates.com',
            'masteraffiliates.com',
            'sportsbettingaffiliates.com',
            'go.affiliatemystake.com',
            'go.affision.com',
            'record.webpartners.co',
            'record.revmasters.com',
            'go.thunder.partners',
            'records.toponepartners.com',
            'link.everygame.eu',
            'record.superiorshare.com'
        ],

        STORAGE_KEYS: {
            VISITOR_ID: 'nb_visitor_id',
            FIRST_VISIT: 'nb_first_visit',
            VISIT_COUNT: 'nb_visit_count',
            LAST_VISIT: 'nb_last_visit'
        },

        DEBUG: true
    };

    // ==========================================
    // INITIALIZATION STATE
    // ==========================================
    var initState = {
        posthogReady: false,
        sessionStarted: false,
        scrollTrackingInit: false,
        ctaTrackingInit: false,
        outboundTrackingInit: false,
        conversionTrackingInit: false,
        sessionEndHandlersInit: false,
        heartbeatInit: false
    };

    // ==========================================
    // STATE
    // ==========================================
    var state = {
        sessionId: null,
        visitorId: null,
        landingTimestamp: null,
        isGoogleReferrer: false,
        referrerDomain: null,
        pageTemplate: null,
        deviceType: null,
        isReturningUser: false,
        visitCount: 1,
        ttfb: null,
        lcp: null,
        fcp: null,
        maxScrollDepth: 0,
        scrollMilestonesReached: {},
        ctasVisible: {},
        ctasVisibleCount: 0,
        ctaClicks: 0,
        firstCtaClickTime: null,
        outboundClicks: 0,
        affiliateClicks: 0,
        hasOutboundClick: false,
        lastOutboundDomain: null,
        conversions: [],
        sessionEnded: false,
        sessionEndSent: false,
        heartbeatCount: 0,
        lastHeartbeatTime: null,
        heartbeatIntervalId: null,
        // v1.3.0: Track tier distribution
        ctaTierDistribution: { 1: 0, 2: 0, 3: 0 }
    };

    // ==========================================
    // UTILITY FUNCTIONS
    // ==========================================
    function generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
    }

    function generateSessionId() {
        return 'nb_' + generateId();
    }

    // ==========================================
    // v1.3.0: 3-TIER CTA IDENTIFICATION SYSTEM
    // ==========================================

    /**
     * Tier 1: Get CTA ID from explicit HTML attributes
     * Priority: data-cta-id > data-cta-name > id
     */
    function getExplicitCtaId(el) {
        // Priority 1: data-cta-id (recommended)
        var explicitId = el.getAttribute('data-cta-id');
        if (explicitId && isValidCtaId(explicitId)) {
            return { id: explicitId, tier: 1, method: 'data-cta-id' };
        }

        // Priority 2: data-cta-name
        var ctaName = el.getAttribute('data-cta-name');
        if (ctaName && isValidCtaId(ctaName)) {
            return { id: ctaName, tier: 1, method: 'data-cta-name' };
        }

        // Priority 3: data-track-id
        var trackId = el.getAttribute('data-track-id');
        if (trackId && isValidCtaId(trackId)) {
            return { id: trackId, tier: 1, method: 'data-track-id' };
        }

        // Priority 4: id attribute (if meaningful, not auto-generated)
        var elementId = el.id;
        if (elementId && isValidCtaId(elementId) && !isAutoGeneratedId(elementId)) {
            return { id: elementId, tier: 1, method: 'element-id' };
        }

        return null;
    }

    /**
     * Validate CTA ID format
     */
    function isValidCtaId(id) {
        return id &&
               id.length > 2 &&
               id.length < 100 &&
               /^[a-zA-Z0-9_-]+$/.test(id);
    }

    /**
     * Detect auto-generated IDs that should be ignored
     */
    function isAutoGeneratedId(id) {
        // Reject WordPress/React auto-generated IDs
        return /^(wp-block-|block-|react-|el-|ember|ng-|uid-|_)\d*/i.test(id) ||
               /^[a-f0-9]{8,}$/i.test(id) ||  // UUID-like
               /^\d+$/.test(id) ||             // Pure numbers
               /^yui_|^ext-gen/i.test(id);     // YUI/ExtJS generated
    }

    /**
     * Tier 2: Derive CTA ID from URL patterns
     */
    function deriveCtaIdFromUrl(href, el) {
        if (!href) return null;

        // Check configurable patterns first
        for (var i = 0; i < CONFIG.AFFILIATE_URL_PATTERNS.length; i++) {
            var patternConfig = CONFIG.AFFILIATE_URL_PATTERNS[i];
            var match = href.match(patternConfig.pattern);
            if (match && match[patternConfig.capture]) {
                return {
                    id: patternConfig.prefix + '_' + match[patternConfig.capture].toLowerCase(),
                    tier: 2,
                    method: 'url-' + patternConfig.prefix + '-pattern',
                    hrefPattern: patternConfig.pattern.toString().split('/')[1].split('(')[0]
                };
            }
        }

        // Social share URLs
        if (/twitter\.com\/intent|x\.com\/intent/i.test(href)) {
            return { id: 'social_twitter', tier: 2, method: 'url-social', hrefPattern: 'twitter-intent' };
        }
        if (/facebook\.com\/sharer/i.test(href)) {
            return { id: 'social_facebook', tier: 2, method: 'url-social', hrefPattern: 'facebook-sharer' };
        }
        if (/linkedin\.com\/share/i.test(href)) {
            return { id: 'social_linkedin', tier: 2, method: 'url-social', hrefPattern: 'linkedin-share' };
        }
        if (/reddit\.com\/submit/i.test(href)) {
            return { id: 'social_reddit', tier: 2, method: 'url-social', hrefPattern: 'reddit-submit' };
        }
        if (/pinterest\.com\/pin\/create/i.test(href)) {
            return { id: 'social_pinterest', tier: 2, method: 'url-social', hrefPattern: 'pinterest-pin' };
        }

        // Known affiliate domains
        for (var j = 0; j < CONFIG.KNOWN_AFFILIATE_DOMAINS.length; j++) {
            var domain = CONFIG.KNOWN_AFFILIATE_DOMAINS[j];
            if (href.toLowerCase().indexOf(domain) !== -1) {
                var domainId = domain.replace(/\./g, '_').replace(/^(go|record|records|link)_/, '');
                return {
                    id: 'affiliate_' + domainId,
                    tier: 2,
                    method: 'url-affiliate-domain',
                    hrefPattern: 'affiliate-domain'
                };
            }
        }

        // External domain (general) - only for actual external links
        try {
            var url = new URL(href, window.location.origin);
            if (url.hostname !== window.location.hostname) {
                var cleanDomain = url.hostname.replace(/^www\./, '').replace(/\./g, '_');
                return {
                    id: 'external_' + cleanDomain,
                    tier: 2,
                    method: 'url-external-domain',
                    hrefPattern: 'external'
                };
            }
        } catch (e) {}

        return null;
    }

    /**
     * Tier 3: Generate fingerprint-based CTA ID
     */
    function generateFingerprintCtaId(el) {
        var ctaType = getCtaType(el);
        var normalizedText = normalizeCtaText(getCtaText(el));
        var region = detectContainerRegion(el);
        var posIndex = getPositionInContainer(el, region);

        // Format: {type}_{text}_{region}_pos{n}
        var id = ctaType;
        if (normalizedText && normalizedText !== 'unnamed') {
            id += '_' + normalizedText;
        }
        if (region && region !== 'content') {
            id += '_' + region;
        }
        if (posIndex > 0) {
            id += '_pos' + posIndex;
        }

        return {
            id: id,
            tier: 3,
            method: 'fingerprint',
            components: {
                type: ctaType,
                text: normalizedText,
                region: region,
                position: posIndex
            }
        };
    }

    /**
     * Normalize CTA text for fingerprint
     */
    function normalizeCtaText(text) {
        if (!text) return 'unnamed';
        return text
            .toLowerCase()
            .trim()
            .substring(0, 20)
            .replace(/[^a-z0-9]+/g, '_')
            .replace(/^_+|_+$/g, '')
            || 'unnamed';
    }

    /**
     * Detect container region for CTA
     */
    function detectContainerRegion(el) {
        var element = el;
        var iterations = 0;

        while (element && element !== document.body && iterations < 20) {
            var tag = element.tagName ? element.tagName.toLowerCase() : '';
            var classes = element.className || '';
            var id = element.id || '';
            var combined = (tag + ' ' + classes + ' ' + id).toLowerCase();

            if (tag === 'header' || /header|masthead|top-bar|site-header/i.test(combined)) {
                return 'header';
            }
            if (tag === 'footer' || /footer|bottom-bar|site-footer/i.test(combined)) {
                return 'footer';
            }
            if (tag === 'aside' || /sidebar|side-bar|widget-area|rail/i.test(combined)) {
                return 'sidebar';
            }
            if (tag === 'nav' || /navigation|menu|navbar|nav-bar/i.test(combined)) {
                return 'nav';
            }
            if (/modal|popup|overlay|dialog|lightbox/i.test(combined)) {
                return 'modal';
            }
            if (/hero|banner|jumbotron|masthead-banner/i.test(combined)) {
                return 'hero';
            }
            if (tag === 'article' || /article|post-content|entry-content|single-content/i.test(combined)) {
                return 'article';
            }
            if (/comment|comments|discussion/i.test(combined)) {
                return 'comments';
            }

            element = element.parentNode;
            iterations++;
        }

        return 'content';
    }

    /**
     * Get position index of CTA within its container
     */
    function getPositionInContainer(el, region) {
        try {
            // Find appropriate container based on region
            var container = document.body;
            if (region === 'header') {
                container = document.querySelector('header, [class*="header"]') || container;
            } else if (region === 'footer') {
                container = document.querySelector('footer, [class*="footer"]') || container;
            } else if (region === 'sidebar') {
                container = document.querySelector('aside, [class*="sidebar"]') || container;
            } else if (region === 'article') {
                container = document.querySelector('article, .post-content, .entry-content') || container;
            }

            // Get all CTAs in container
            var selectorString = CONFIG.CTA_SELECTORS.join(',');
            var allCtas;
            try {
                allCtas = container.querySelectorAll(selectorString);
            } catch (e) {
                allCtas = [];
            }

            for (var i = 0; i < allCtas.length; i++) {
                if (allCtas[i] === el) {
                    return i + 1;
                }
            }
        } catch (e) {
            logError('getPositionInContainer', e);
        }

        return 0;
    }

    /**
     * Master CTA ID Generator - Uses 3-tier fallback system
     * @param {HTMLElement} el - The CTA element
     * @returns {Object} { id, tier, method, [components], [hrefPattern] }
     */
    function generateSmartCtaId(el) {
        // Tier 1: Explicit HTML attributes
        var tier1Result = getExplicitCtaId(el);
        if (tier1Result) {
            log('CTA ID (Tier 1):', tier1Result.id, 'via', tier1Result.method);
            state.ctaTierDistribution[1]++;
            return tier1Result;
        }

        // Tier 2: URL pattern derivation
        var href = el.href || el.getAttribute('href') || '';
        var tier2Result = deriveCtaIdFromUrl(href, el);
        if (tier2Result) {
            log('CTA ID (Tier 2):', tier2Result.id, 'via', tier2Result.method);
            state.ctaTierDistribution[2]++;
            return tier2Result;
        }

        // Tier 3: Position + element fingerprint
        var tier3Result = generateFingerprintCtaId(el);
        log('CTA ID (Tier 3):', tier3Result.id, 'via fingerprint');
        state.ctaTierDistribution[3]++;
        return tier3Result;
    }

    // ==========================================
    // VISITOR IDENTIFICATION
    // ==========================================
    function getOrCreateVisitorId() {
        try {
            var visitorId = localStorage.getItem(CONFIG.STORAGE_KEYS.VISITOR_ID);
            if (!visitorId) {
                visitorId = 'v_' + generateId();
                localStorage.setItem(CONFIG.STORAGE_KEYS.VISITOR_ID, visitorId);
                localStorage.setItem(CONFIG.STORAGE_KEYS.FIRST_VISIT, new Date().toISOString());
                localStorage.setItem(CONFIG.STORAGE_KEYS.VISIT_COUNT, '1');
            } else {
                var count = parseInt(localStorage.getItem(CONFIG.STORAGE_KEYS.VISIT_COUNT) || '1', 10);
                localStorage.setItem(CONFIG.STORAGE_KEYS.VISIT_COUNT, String(count + 1));
            }
            localStorage.setItem(CONFIG.STORAGE_KEYS.LAST_VISIT, new Date().toISOString());
            return visitorId;
        } catch (e) {
            logError('getOrCreateVisitorId', e);
            return 'v_anon_' + generateId();
        }
    }

    function isReturningVisitor() {
        try {
            return parseInt(localStorage.getItem(CONFIG.STORAGE_KEYS.VISIT_COUNT) || '1', 10) > 1;
        } catch (e) {
            return false;
        }
    }

    function getVisitCount() {
        try {
            return parseInt(localStorage.getItem(CONFIG.STORAGE_KEYS.VISIT_COUNT) || '1', 10);
        } catch (e) {
            return 1;
        }
    }

    function getFirstVisitDate() {
        try {
            return localStorage.getItem(CONFIG.STORAGE_KEYS.FIRST_VISIT) || null;
        } catch (e) {
            return null;
        }
    }

    // ==========================================
    // PERFORMANCE METRICS
    // ==========================================
    function getPerformanceMetrics() {
        var metrics = { ttfb: null, lcp: null, fcp: null };
        try {
            if (typeof performance !== 'undefined' && performance.getEntriesByType) {
                var navEntries = performance.getEntriesByType('navigation');
                if (navEntries && navEntries.length > 0) {
                    metrics.ttfb = Math.round(navEntries[0].responseStart - navEntries[0].requestStart);
                }
                var paintEntries = performance.getEntriesByType('paint');
                if (paintEntries) {
                    for (var i = 0; i < paintEntries.length; i++) {
                        if (paintEntries[i].name === 'first-contentful-paint') {
                            metrics.fcp = Math.round(paintEntries[i].startTime);
                            break;
                        }
                    }
                }
            }
        } catch (e) {
            logError('getPerformanceMetrics', e);
        }
        return metrics;
    }

    function observeLCP() {
        try {
            if (typeof PerformanceObserver === 'undefined') return;
            var observer = new PerformanceObserver(function(list) {
                var entries = list.getEntries();
                var lastEntry = entries[entries.length - 1];
                if (lastEntry) state.lcp = Math.round(lastEntry.startTime);
            });
            observer.observe({ type: 'largest-contentful-paint', buffered: true });
        } catch (e) {
            logError('observeLCP', e);
        }
    }

    // ==========================================
    // DETECTION FUNCTIONS
    // ==========================================
    function isGoogleReferrer(referrer) {
        if (!referrer) return false;
        try {
            var urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('gclid')) return true;
            var utmSource = urlParams.get('utm_source');
            if (utmSource && utmSource.toLowerCase() === 'google') return true;
        } catch (e) {}
        try {
            var url = new URL(referrer);
            for (var i = 0; i < CONFIG.GOOGLE_DOMAINS.length; i++) {
                if (url.hostname.indexOf(CONFIG.GOOGLE_DOMAINS[i]) !== -1) return true;
            }
        } catch (e) {
            return referrer.toLowerCase().indexOf('google') !== -1;
        }
        return false;
    }

    function getReferrerDomain(referrer) {
        if (!referrer) return 'direct';
        try {
            return new URL(referrer).hostname;
        } catch (e) {
            return 'unknown';
        }
    }

    function detectPageTemplate() {
        var path = window.location.pathname;
        var classes = document.body ? document.body.className : '';
        if (classes.indexOf('single-post') !== -1 || classes.indexOf('single') !== -1) return 'article';
        if (classes.indexOf('archive') !== -1 || classes.indexOf('category') !== -1) return 'category';
        if (classes.indexOf('home') !== -1 || classes.indexOf('front-page') !== -1) return 'homepage';
        if (classes.indexOf('search-results') !== -1) return 'search';
        if (classes.indexOf('author') !== -1) return 'author';
        if (path === '/' || path === '/index.html') return 'homepage';
        if (/^\/\d{4}\/\d{2}\/\d{2}\//.test(path)) return 'article';
        if (path.indexOf('/category/') !== -1) return 'category';
        if (path.indexOf('/news/') !== -1) return 'news';
        if (document.querySelector('article.post') || document.querySelector('.post-content')) return 'article';
        return 'page';
    }

    function detectDeviceType() {
        var ua = navigator.userAgent;
        if (/Mobile|Android|iPhone|iPod/i.test(ua)) return 'mobile';
        if (/iPad|Tablet/i.test(ua)) return 'tablet';
        return 'desktop';
    }

    function getScrollDepthPercent() {
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop || 0;
        var docHeight = Math.max(
            document.body ? document.body.scrollHeight : 0,
            document.documentElement ? document.documentElement.scrollHeight : 0
        );
        var winHeight = window.innerHeight || 0;
        var scrollable = docHeight - winHeight;
        if (scrollable <= 0) return 100;
        return Math.min(Math.round((scrollTop / scrollable) * 100), 100);
    }

    function getDwellRating(ms) {
        if (ms < CONFIG.DWELL_BENCHMARKS.VERY_BAD) return 'very_bad';
        if (ms < CONFIG.DWELL_BENCHMARKS.WEAK) return 'weak';
        if (ms < CONFIG.DWELL_BENCHMARKS.NORMAL) return 'normal';
        return 'strong';
    }

    function isExternalLink(href) {
        try {
            var url = new URL(href, window.location.origin);
            return url.hostname !== window.location.hostname;
        } catch (e) {
            return false;
        }
    }

    function isAffiliateLink(href, el) {
        if (!href) return false;
        if (/\/go\/|\/out\/|\/aff\/|\/partner\/|\?ref=|\?aff=|affiliate|sponsored/i.test(href)) return true;
        if (el && el.rel && /sponsored|nofollow/i.test(el.rel)) return true;
        return false;
    }

    // ==========================================
    // POSTHOG EVENT TRACKING
    // ==========================================
    function trackEvent(eventName, properties) {
        properties = properties || {};
        if (typeof posthog === 'undefined') {
            log('PostHog not loaded, event skipped:', eventName);
            return false;
        }
        var baseProperties = {
            session_id: state.sessionId,
            visitor_id: state.visitorId,
            page_template: state.pageTemplate,
            referrer_domain: state.referrerDomain,
            is_google_referrer: state.isGoogleReferrer,
            is_returning_user: state.isReturningUser,
            device_type: state.deviceType,
            page_url: window.location.href,
            page_path: window.location.pathname,
            site_vertical: CONFIG.VERTICAL,
            tracker_version: VERSION
        };
        for (var key in properties) {
            if (properties.hasOwnProperty(key)) baseProperties[key] = properties[key];
        }
        try {
            posthog.capture(eventName, baseProperties);
            log('Event:', eventName, properties);
            return true;
        } catch (e) {
            logError('trackEvent:' + eventName, e);
            return false;
        }
    }

    function trackEventWithBeacon(eventName, properties) {
        properties = properties || {};
        if (typeof posthog === 'undefined') return false;

        var baseProperties = {
            session_id: state.sessionId,
            visitor_id: state.visitorId,
            page_template: state.pageTemplate,
            referrer_domain: state.referrerDomain,
            is_google_referrer: state.isGoogleReferrer,
            is_returning_user: state.isReturningUser,
            device_type: state.deviceType,
            page_url: window.location.href,
            page_path: window.location.pathname,
            site_vertical: CONFIG.VERTICAL,
            tracker_version: VERSION
        };
        for (var key in properties) {
            if (properties.hasOwnProperty(key)) baseProperties[key] = properties[key];
        }

        try {
            posthog.capture(eventName, baseProperties, { transport: 'sendBeacon' });
            return true;
        } catch (e) {
            logError('trackEventWithBeacon:' + eventName, e);
        }

        try {
            posthog.capture(eventName, baseProperties);
            return true;
        } catch (e) {
            logError('trackEventWithBeacon fallback:' + eventName, e);
            return false;
        }
    }

    // ==========================================
    // SESSION START
    // ==========================================
    function startSession() {
        try {
            state.sessionId = generateSessionId();
            state.visitorId = getOrCreateVisitorId();
            state.landingTimestamp = Date.now();
            state.referrerDomain = getReferrerDomain(document.referrer);
            state.isGoogleReferrer = isGoogleReferrer(document.referrer);
            state.pageTemplate = detectPageTemplate();
            state.deviceType = detectDeviceType();
            state.isReturningUser = isReturningVisitor();
            state.visitCount = getVisitCount();

            var perfMetrics = getPerformanceMetrics();
            state.ttfb = perfMetrics.ttfb;
            state.fcp = perfMetrics.fcp;

            trackEvent('navboost:session_start', {
                landing_timestamp: state.landingTimestamp,
                referrer: document.referrer,
                landing_page: window.location.pathname,
                first_visit_date: getFirstVisitDate(),
                visit_count: state.visitCount,
                ttfb_ms: state.ttfb,
                fcp_ms: state.fcp
            });

            observeLCP();
            initState.sessionStarted = true;
            logInit('Session started: ' + state.sessionId);
            return true;
        } catch (e) {
            logError('startSession', e);
            return false;
        }
    }

    // ==========================================
    // SESSION END
    // ==========================================
    function buildSessionEndData(trigger) {
        var dwellTimeMs = Date.now() - state.landingTimestamp;
        var dwellTimeSeconds = Math.round(dwellTimeMs / 1000);
        var isPogo = state.isGoogleReferrer && dwellTimeMs < CONFIG.POGO_THRESHOLD_MS && !state.hasOutboundClick && state.maxScrollDepth < 25;
        var isGoodAbandonment = state.isGoogleReferrer && state.hasOutboundClick;
        var sessionCtaCtr = state.ctasVisibleCount > 0 ? Math.round((state.ctaClicks / state.ctasVisibleCount) * 100 * 10) / 10 : 0;

        var milestonesArray = [];
        for (var m in state.scrollMilestonesReached) {
            if (state.scrollMilestonesReached.hasOwnProperty(m) && state.scrollMilestonesReached[m]) {
                milestonesArray.push(parseInt(m, 10));
            }
        }

        return {
            dwell_time_seconds: dwellTimeSeconds,
            dwell_time_ms: dwellTimeMs,
            dwell_rating: getDwellRating(dwellTimeMs),
            is_pogo: isPogo,
            is_good_abandonment: isGoodAbandonment,
            scroll_depth_reached: state.maxScrollDepth,
            scroll_milestones: milestonesArray,
            ctas_visible: state.ctasVisibleCount,
            cta_clicks: state.ctaClicks,
            session_cta_ctr: sessionCtaCtr,
            time_to_first_cta: state.firstCtaClickTime ? Math.round((state.firstCtaClickTime - state.landingTimestamp) / 1000) : null,
            had_outbound_click: state.hasOutboundClick,
            outbound_clicks: state.outboundClicks,
            affiliate_clicks: state.affiliateClicks,
            last_outbound_domain: state.lastOutboundDomain,
            conversions: state.conversions,
            conversion_count: state.conversions.length,
            ttfb_ms: state.ttfb,
            lcp_ms: state.lcp,
            fcp_ms: state.fcp,
            exit_trigger: trigger,
            heartbeat_count: state.heartbeatCount,
            // v1.3.0: Include tier distribution
            cta_tier_distribution: state.ctaTierDistribution,
            init_state: initState
        };
    }

    function endSession(trigger) {
        if (state.sessionEndSent) return;
        state.sessionEndSent = true;
        state.sessionEnded = true;

        try {
            var sessionEndData = buildSessionEndData(trigger);
            trackEventWithBeacon('navboost:session_end', sessionEndData);
            logInit('Session ended: dwell=' + sessionEndData.dwell_time_seconds + 's, trigger=' + trigger);
        } catch (e) {
            logError('endSession', e);
        }
    }

    // ==========================================
    // HEARTBEAT (v1.1.2)
    // ==========================================
    function sendHeartbeat() {
        if (state.sessionEnded) return;
        state.heartbeatCount++;
        state.lastHeartbeatTime = Date.now();

        try {
            var heartbeatData = buildSessionEndData('heartbeat');
            heartbeatData.heartbeat_number = state.heartbeatCount;
            trackEvent('navboost:heartbeat', heartbeatData);
            log('Heartbeat #' + state.heartbeatCount);
        } catch (e) {
            logError('sendHeartbeat', e);
        }
    }

    function initHeartbeat() {
        try {
            state.heartbeatIntervalId = setInterval(sendHeartbeat, CONFIG.HEARTBEAT_INTERVAL_MS);
            initState.heartbeatInit = true;
            logInit('Heartbeat initialized (every ' + (CONFIG.HEARTBEAT_INTERVAL_MS / 1000) + 's)');
            return true;
        } catch (e) {
            logError('initHeartbeat', e);
            return false;
        }
    }

    // ==========================================
    // SCROLL TRACKING
    // ==========================================
    function initScrollTracking() {
        try {
            var ticking = false;
            function onScroll() {
                if (!ticking) {
                    if (typeof window.requestAnimationFrame === 'function') {
                        window.requestAnimationFrame(function() {
                            processScroll();
                            ticking = false;
                        });
                    } else {
                        processScroll();
                    }
                    ticking = true;
                }
            }

            function processScroll() {
                try {
                    var currentDepth = getScrollDepthPercent();
                    if (currentDepth > state.maxScrollDepth) state.maxScrollDepth = currentDepth;

                    for (var i = 0; i < CONFIG.SCROLL_MILESTONES.length; i++) {
                        var milestone = CONFIG.SCROLL_MILESTONES[i];
                        if (currentDepth >= milestone && !state.scrollMilestonesReached[milestone]) {
                            state.scrollMilestonesReached[milestone] = true;
                            trackEvent('navboost:scroll_zone', {
                                scroll_depth_percent: milestone,
                                scroll_zone: CONFIG.SCROLL_ZONES[milestone],
                                time_to_scroll: Math.round((Date.now() - state.landingTimestamp) / 1000)
                            });
                        }
                    }
                } catch (e) {
                    logError('processScroll', e);
                }
            }

            window.addEventListener('scroll', onScroll, { passive: true });
            setTimeout(onScroll, 100);
            initState.scrollTrackingInit = true;
            logInit('Scroll tracking initialized');
            return true;
        } catch (e) {
            logError('initScrollTracking', e);
            return false;
        }
    }

    // ==========================================
    // CTA TRACKING - v1.3.0 SMART CTA DETECTION
    // ==========================================

    // Test if element matches ANY selector individually
    function elementMatchesCTA(el) {
        if (!el || !el.matches) return false;

        for (var i = 0; i < CONFIG.CTA_SELECTORS.length; i++) {
            try {
                if (el.matches(CONFIG.CTA_SELECTORS[i])) {
                    return true;
                }
            } catch (e) {
                log('Selector failed:', CONFIG.CTA_SELECTORS[i], e.message);
            }
        }
        return false;
    }

    // Find closest CTA element by walking up the DOM
    function findClosestCTA(target) {
        var el = target;
        var iterations = 0;
        var maxIterations = 10;

        while (el && el !== document && iterations < maxIterations) {
            if (elementMatchesCTA(el)) {
                return el;
            }
            el = el.parentNode;
            iterations++;
        }
        return null;
    }

    function initCTATracking() {
        try {
            // Check for IntersectionObserver
            if (typeof IntersectionObserver === 'undefined') {
                logInit('IntersectionObserver not supported');
                initState.ctaTrackingInit = true;
                return true;
            }

            // Build selector for querySelectorAll
            var selectorString = CONFIG.CTA_SELECTORS.join(',');

            // Visibility tracking
            var observer = new IntersectionObserver(function(entries) {
                for (var i = 0; i < entries.length; i++) {
                    try {
                        var entry = entries[i];
                        if (entry.isIntersecting) {
                            var el = entry.target;

                            // v1.3.0: Use smart CTA ID generation
                            var ctaIdResult = generateSmartCtaId(el);
                            var ctaId = ctaIdResult.id;

                            if (!state.ctasVisible[ctaId]) {
                                state.ctasVisible[ctaId] = true;
                                state.ctasVisibleCount++;

                                var ctaText = getCtaText(el);
                                var region = detectContainerRegion(el);
                                var position = getPositionInContainer(el, region);

                                if (ctaText && ctaText.length > 0) {
                                    trackEvent('navboost:cta_visible', {
                                        cta_id: ctaId,
                                        cta_id_tier: ctaIdResult.tier,
                                        cta_id_method: ctaIdResult.method,
                                        cta_type: getCtaType(el),
                                        cta_text: ctaText,
                                        cta_href: el.href || null,
                                        cta_region: region,
                                        cta_position: position,
                                        cta_href_pattern: ctaIdResult.hrefPattern || null,
                                        time_to_visibility: Math.round((Date.now() - state.landingTimestamp) / 1000)
                                    });
                                }
                            }
                        }
                    } catch (e) {
                        logError('CTA observer entry', e);
                    }
                }
            }, { threshold: 0.5 });

            // Find and observe CTA elements
            var elements;
            try {
                elements = document.querySelectorAll(selectorString);
            } catch (e) {
                logError('querySelectorAll CTA', e);
                elements = [];
            }

            logInit('Found ' + elements.length + ' CTA elements');

            for (var j = 0; j < elements.length; j++) {
                try {
                    observer.observe(elements[j]);
                } catch (e) {
                    logError('observe CTA element', e);
                }
            }

            // Click tracking
            document.addEventListener('click', handleCtaClick, true);

            initState.ctaTrackingInit = true;
            logInit('CTA tracking initialized with ' + elements.length + ' elements');
            return true;
        } catch (e) {
            logError('initCTATracking', e);
            return false;
        }
    }

    // v1.3.0: Enhanced click handler with smart CTA ID
    function handleCtaClick(e) {
        try {
            var target = e.target;
            var ctaElement = findClosestCTA(target);

            if (ctaElement) {
                state.ctaClicks++;
                if (!state.firstCtaClickTime) state.firstCtaClickTime = Date.now();

                var ctaText = getCtaText(ctaElement);

                // v1.3.0: Use smart CTA ID generation
                var ctaIdResult = generateSmartCtaId(ctaElement);
                var region = detectContainerRegion(ctaElement);
                var position = getPositionInContainer(ctaElement, region);

                trackEvent('navboost:cta_click', {
                    cta_id: ctaIdResult.id,
                    cta_id_tier: ctaIdResult.tier,
                    cta_id_method: ctaIdResult.method,
                    cta_text: ctaText,
                    cta_type: getCtaType(ctaElement),
                    cta_href: ctaElement.href || null,
                    cta_region: region,
                    cta_position: position,
                    cta_href_pattern: ctaIdResult.hrefPattern || null,
                    time_to_click: Math.round((Date.now() - state.landingTimestamp) / 1000),
                    was_visible: !!state.ctasVisible[ctaIdResult.id],
                    click_target_tag: target.tagName
                });

                log('CTA click captured:', ctaText, '| ID:', ctaIdResult.id, '| Tier:', ctaIdResult.tier);
            }
        } catch (e) {
            logError('handleCtaClick', e);
        }
    }

    function getCtaText(el) {
        try {
            var text = (el.innerText || '').trim();
            if (text && text.length > 0 && text.length < 100) return text.substring(0, 50);
            text = (el.value || el.title || el.getAttribute('aria-label') || '').trim();
            if (text) return text.substring(0, 50);
            var img = el.querySelector('img');
            if (img && img.alt) return img.alt.substring(0, 50);
        } catch (e) {
            logError('getCtaText', e);
        }
        return '';
    }

    function getCtaType(el) {
        var tag = el.tagName ? el.tagName.toLowerCase() : 'unknown';
        var href = el.href || '';
        var classes = el.className || '';

        if (href.indexOf('twitter.com') !== -1 || href.indexOf('x.com') !== -1) return 'social_twitter';
        if (href.indexOf('facebook.com/sharer') !== -1) return 'social_facebook';
        if (href.indexOf('linkedin.com/share') !== -1) return 'social_linkedin';
        if (href.indexOf('reddit.com/submit') !== -1) return 'social_reddit';
        if (href.indexOf('mailto:') !== -1) return 'email';

        if (classes.indexOf('newsletter') !== -1 || classes.indexOf('subscribe') !== -1) return 'newsletter';
        if (classes.indexOf('share') !== -1 || classes.indexOf('social') !== -1) return 'social_share';
        if (classes.indexOf('read-more') !== -1 || classes.indexOf('more-link') !== -1) return 'read_more';
        if (classes.indexOf('related') !== -1) return 'related_link';
        if (classes.indexOf('search') !== -1) return 'search';
        if (classes.indexOf('comment') !== -1) return 'comment';
        if (classes.indexOf('promo') !== -1 || classes.indexOf('play-now') !== -1) return 'affiliate';
        if (classes.indexOf('affiliate') !== -1) return 'affiliate';

        if (tag === 'button' || (tag === 'input' && el.type === 'submit')) return 'button';
        if (tag === 'a') return 'link';

        return tag;
    }

    // ==========================================
    // OUTBOUND TRACKING
    // ==========================================
    function initOutboundTracking() {
        try {
            document.addEventListener('click', handleOutboundClick, true);
            initState.outboundTrackingInit = true;
            logInit('Outbound tracking initialized');
            return true;
        } catch (e) {
            logError('initOutboundTracking', e);
            return false;
        }
    }

    function handleOutboundClick(e) {
        try {
            var link = e.target;
            var iterations = 0;
            while (link && link.tagName !== 'A' && link !== document && iterations < 10) {
                link = link.parentNode;
                iterations++;
            }

            if (!link || link.tagName !== 'A' || !link.href) return;

            var href = link.href;
            if (!isExternalLink(href)) return;

            state.outboundClicks++;
            state.hasOutboundClick = true;

            var isAffiliate = isAffiliateLink(href, link);
            if (isAffiliate) state.affiliateClicks++;

            var outboundDomain = 'unknown';
            try {
                outboundDomain = new URL(href).hostname;
            } catch (e) {}
            state.lastOutboundDomain = outboundDomain;

            var linkType = 'external';
            if (isAffiliate) linkType = 'affiliate';
            else if (href.indexOf('twitter.com') !== -1 || href.indexOf('facebook.com') !== -1) linkType = 'social';

            trackEvent('navboost:outbound_click', {
                outbound_url: href,
                outbound_domain: outboundDomain,
                link_type: linkType,
                is_affiliate: isAffiliate,
                link_text: (link.innerText || '').trim().substring(0, 50),
                time_to_click: Math.round((Date.now() - state.landingTimestamp) / 1000)
            });

            log('Outbound click:', outboundDomain);
        } catch (e) {
            logError('handleOutboundClick', e);
        }
    }

    // ==========================================
    // CONVERSION TRACKING
    // ==========================================
    function initConversionTracking() {
        try {
            var newsletterForms = document.querySelectorAll('form[action*="newsletter"], form[action*="subscribe"], .mc4wp-form, .newsletter-form');
            for (var i = 0; i < newsletterForms.length; i++) {
                (function(form) {
                    form.addEventListener('submit', function() {
                        state.conversions.push({ type: 'newsletter', time: Date.now() });
                        trackEvent('conversion:newsletter_signup', {
                            conversion_type: 'newsletter',
                            time_to_convert: Math.round((Date.now() - state.landingTimestamp) / 1000)
                        });
                    });
                })(newsletterForms[i]);
            }

            var contentConsumed = false;
            window.addEventListener('scroll', function() {
                if (!contentConsumed && state.maxScrollDepth >= 90) {
                    contentConsumed = true;
                    state.conversions.push({ type: 'content_consumed', time: Date.now() });
                    trackEvent('conversion:content_consumed', {
                        conversion_type: 'content_consumed',
                        scroll_depth: state.maxScrollDepth,
                        time_to_consume: Math.round((Date.now() - state.landingTimestamp) / 1000)
                    });
                }
            }, { passive: true });

            initState.conversionTrackingInit = true;
            logInit('Conversion tracking initialized');
            return true;
        } catch (e) {
            logError('initConversionTracking', e);
            return false;
        }
    }

    // ==========================================
    // v1.3.0: DIAGNOSTIC MODE
    // ==========================================
    function runCtaDiagnostic() {
        var allLinks = document.querySelectorAll('a[href], button');
        var selectorString = CONFIG.CTA_SELECTORS.join(',');
        var ctaElements;
        try {
            ctaElements = document.querySelectorAll(selectorString);
        } catch (e) {
            ctaElements = [];
        }

        var diagnosticData = {
            total_links: allLinks.length,
            detected_ctas: ctaElements.length,
            detection_rate: Math.round((ctaElements.length / allLinks.length) * 100),
            cta_breakdown: {},
            undetected_potential_ctas: [],
            tier_distribution: { 1: 0, 2: 0, 3: 0 },
            cta_details: []
        };

        // Analyze detected CTAs
        for (var i = 0; i < ctaElements.length; i++) {
            var el = ctaElements[i];
            var ctaIdResult = generateSmartCtaId(el);
            diagnosticData.tier_distribution[ctaIdResult.tier]++;

            var type = getCtaType(el);
            diagnosticData.cta_breakdown[type] = (diagnosticData.cta_breakdown[type] || 0) + 1;

            diagnosticData.cta_details.push({
                id: ctaIdResult.id,
                tier: ctaIdResult.tier,
                method: ctaIdResult.method,
                type: type,
                text: getCtaText(el).substring(0, 30),
                href: (el.href || '').substring(0, 50),
                region: detectContainerRegion(el)
            });
        }

        // Find potential undetected CTAs
        for (var j = 0; j < allLinks.length; j++) {
            var link = allLinks[j];
            if (!elementMatchesCTA(link)) {
                var href = link.href || '';
                // Check if it looks like an affiliate link
                if (/\/go\/|\/out\/|affiliate|sponsored/i.test(href) ||
                    (link.rel && /sponsored|nofollow/i.test(link.rel))) {
                    diagnosticData.undetected_potential_ctas.push({
                        href: href.substring(0, 80),
                        text: (link.innerText || '').substring(0, 50),
                        classes: (link.className || '').substring(0, 50),
                        suggestion: 'Add to CTA_SELECTORS or use data-cta-id'
                    });
                }
            }
        }

        trackEvent('navboost:cta_diagnostic', diagnosticData);

        // Pretty console output
        console.group('[NavBoost v' + VERSION + '] CTA Diagnostic Report');
        console.log('Total links:', diagnosticData.total_links);
        console.log('Detected CTAs:', diagnosticData.detected_ctas);
        console.log('Detection rate:', diagnosticData.detection_rate + '%');
        console.log('Tier distribution:', diagnosticData.tier_distribution);
        console.table(diagnosticData.cta_breakdown);
        if (diagnosticData.undetected_potential_ctas.length > 0) {
            console.warn('Potential undetected CTAs:');
            console.table(diagnosticData.undetected_potential_ctas);
        }
        console.log('CTA Details:');
        console.table(diagnosticData.cta_details);
        console.groupEnd();

        return diagnosticData;
    }

    // Expose diagnostic function globally
    window.navboostDiagnostic = runCtaDiagnostic;

    // ==========================================
    // INITIALIZATION
    // ==========================================
    function init() {
        logInit('Starting initialization...');

        if (typeof posthog === 'undefined') {
            logInit('Waiting for PostHog...');
            setTimeout(init, 100);
            return;
        }

        initState.posthogReady = true;
        logInit('PostHog ready, initializing tracker v' + VERSION);

        try {
            posthog.capture('navboost:init_start', {
                tracker_version: VERSION,
                page_url: window.location.href
            });
        } catch (e) {
            logError('init_start event', e);
        }

        var initResults = {
            session: false,
            scroll: false,
            cta: false,
            outbound: false,
            conversion: false,
            heartbeat: false
        };

        try { initResults.session = startSession(); } catch (e) { logError('startSession wrapper', e); }
        try { initResults.scroll = initScrollTracking(); } catch (e) { logError('initScrollTracking wrapper', e); }
        try { initResults.cta = initCTATracking(); } catch (e) { logError('initCTATracking wrapper', e); }
        try { initResults.outbound = initOutboundTracking(); } catch (e) { logError('initOutboundTracking wrapper', e); }
        try { initResults.conversion = initConversionTracking(); } catch (e) { logError('initConversionTracking wrapper', e); }
        try { initResults.heartbeat = initHeartbeat(); } catch (e) { logError('initHeartbeat wrapper', e); }

        // Session end handlers
        try {
            document.addEventListener('visibilitychange', function() {
                if (document.visibilityState === 'hidden') endSession('visibilitychange');
            });
            window.addEventListener('pagehide', function() { endSession('pagehide'); });
            window.addEventListener('beforeunload', function() { endSession('beforeunload'); });
            initState.sessionEndHandlersInit = true;
            logInit('Session end handlers initialized');
        } catch (e) {
            logError('session end handlers', e);
        }

        try {
            posthog.capture('navboost:init_complete', {
                tracker_version: VERSION,
                init_results: initResults,
                init_state: initState
            });
        } catch (e) {
            logError('init_complete event', e);
        }

        logInit('NavBoost Tracker v' + VERSION + ' initialization complete');
        logInit('Init results: ' + JSON.stringify(initResults));
        logInit('Run window.navboostDiagnostic() for CTA detection analysis');
    }

    // Start
    logInit('Script loaded, waiting for DOM...');
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
