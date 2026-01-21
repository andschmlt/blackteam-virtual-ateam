/**
 * NavBoost Tracker - northeasttimes.com
 * Site Type: Local News
 * Vertical: news
 * PostHog Project ID: 290039
 * Generated: 2026-01-21
 *
 * Full NavBoost KPI Framework implementation
 */

(function() {
    'use strict';

    const CONFIG = {
        SITE_DOMAIN: 'northeasttimes.com',
        SITE_TYPE: 'Local News',
        VERTICAL: 'news',
        POGO_THRESHOLD_MS: 8000,
        SCROLL_MILESTONES: [25, 50, 75, 100],
        SCROLL_ZONES: { 25: 'above_fold', 50: 'cta_zone', 75: 'content', 100: 'footer' },
        GOOGLE_DOMAINS: ['google.com', 'google.co.uk', 'google.de', 'google.fr', 'google.es', 'google.it', 'google.nl', 'google.com.au', 'google.ca'],
        DWELL_BENCHMARKS: { VERY_BAD: 10000, WEAK: 30000, NORMAL: 60000, STRONG: 60001 },
        TARGETS: { POGO_RATE: 20, DWELL_TIME: 60, CTA_CTR: 3, ENGAGEMENT_SCORE: 65, GOOD_ABANDONMENT: 10 },
        CTA_SELECTORS: [
            '.newsletter-signup', '.subscribe-btn', '.email-signup', 'form[action*="newsletter"]', 'form[action*="subscribe"]', '.mc4wp-form',
            '.share-button', '.social-share', 'a[href*="twitter.com/intent"]', 'a[href*="facebook.com/sharer"]',
            '.read-more', '.continue-reading', '.related-article a', '.cta-button', '.btn-primary', 'a.button', 'button[type="submit"]'
        ],
        OUTBOUND_PATTERNS: [/^https?:\/\/(?!.*northeasttimes\\.com)/i, /\/go\//i, /\/out\//i, /\/aff\//i],
        CONVERSION_FORMS: {
            newsletter: ['form[action*="newsletter"]', 'form[action*="subscribe"]', '.mc4wp-form'],
            contact: ['form[action*="contact"]', '.contact-form', '.wpcf7-form'],
            comment: ['#commentform', 'form.comment-form'],
            search: ['form[role="search"]', 'form.search-form', '#searchform']
        },
        DEBUG: false
    };

    const state = {
        sessionId: null, landingTimestamp: null, isGoogleReferrer: false, referrerDomain: null, pageTemplate: null, deviceType: null,
        maxScrollDepth: 0, scrollMilestonesReached: new Set(), ctasVisible: new Set(), ctaClicks: 0, firstCtaClickTime: null,
        outboundClicks: 0, affiliateClicks: 0, hasOutboundClick: false, conversions: [], sessionEnded: false
    };

    function log(...args) { if (CONFIG.DEBUG) console.log('[NavBoost]', ...args); }
    function generateSessionId() { return 'nb_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9); }
    function isGoogleReferrer(referrer) {
        if (!referrer) return false;
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('gclid') || urlParams.get('utm_source')?.toLowerCase() === 'google') return true;
        try { const url = new URL(referrer); return CONFIG.GOOGLE_DOMAINS.some(domain => url.hostname.includes(domain)); }
        catch { return referrer.toLowerCase().includes('google'); }
    }
    function getReferrerDomain(referrer) { if (!referrer) return 'direct'; try { return new URL(referrer).hostname; } catch { return 'unknown'; } }
    function detectPageTemplate() {
        const path = window.location.pathname; const body = document.body; const classes = body.className;
        if (classes.includes('single-post') || classes.includes('single')) return 'article';
        if (classes.includes('archive') || classes.includes('category')) return 'category';
        if (path === '/' || path === '/index.html') return 'homepage';
        if (path.match(/^\/\d{4}\/\d{2}\/\d{2}\//)) return 'article';
        if (path.includes('/category/')) return 'category';
        if (document.querySelector('article')) return 'article';
        return 'page';
    }
    function detectDeviceType() { const ua = navigator.userAgent; if (/Mobile|Android|iPhone/i.test(ua)) return 'mobile'; if (/iPad|Tablet/i.test(ua)) return 'tablet'; return 'desktop'; }
    function getScrollDepthPercent() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const docHeight = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, document.body.offsetHeight, document.documentElement.offsetHeight);
        const winHeight = window.innerHeight; const scrollable = docHeight - winHeight;
        if (scrollable <= 0) return 100; return Math.min(Math.round((scrollTop / scrollable) * 100), 100);
    }
    function getDwellRating(ms) { if (ms < CONFIG.DWELL_BENCHMARKS.VERY_BAD) return 'very_bad'; if (ms < CONFIG.DWELL_BENCHMARKS.WEAK) return 'weak'; if (ms < CONFIG.DWELL_BENCHMARKS.NORMAL) return 'normal'; return 'strong'; }
    function isAffiliateLink(href) { if (!href) return false; return /\/go\/|\/out\/|\/aff\/|\/partner\/|\?ref=|\?aff=/i.test(href); }
    function isOutboundLink(href) { if (!href) return false; return CONFIG.OUTBOUND_PATTERNS.some(pattern => pattern.test(href)); }

    function trackEvent(eventName, properties = {}) {
        if (typeof posthog === 'undefined') return;
        const baseProperties = { session_id: state.sessionId, page_template: state.pageTemplate, referrer_domain: state.referrerDomain, is_google_referrer: state.isGoogleReferrer, device_type: state.deviceType, page_url: window.location.href, page_path: window.location.pathname, site_vertical: CONFIG.VERTICAL };
        posthog.capture(eventName, { ...baseProperties, ...properties });
        log('Event:', eventName, properties);
    }

    function startSession() {
        state.sessionId = generateSessionId(); state.landingTimestamp = Date.now(); state.referrerDomain = getReferrerDomain(document.referrer);
        state.isGoogleReferrer = isGoogleReferrer(document.referrer); state.pageTemplate = detectPageTemplate(); state.deviceType = detectDeviceType();
        trackEvent('navboost:session_start', { landing_timestamp: state.landingTimestamp, referrer: document.referrer, landing_page: window.location.pathname });
        log('Session started:', state.sessionId);
    }

    function endSession() {
        if (state.sessionEnded) return; state.sessionEnded = true;
        const dwellTimeMs = Date.now() - state.landingTimestamp; const dwellTimeSeconds = Math.round(dwellTimeMs / 1000);
        const isPogo = state.isGoogleReferrer && dwellTimeMs < CONFIG.POGO_THRESHOLD_MS && !state.hasOutboundClick && state.maxScrollDepth < 25;
        const isGoodAbandonment = state.isGoogleReferrer && state.hasOutboundClick;
        trackEvent('navboost:session_end', {
            dwell_time_seconds: dwellTimeSeconds, dwell_time_ms: dwellTimeMs, dwell_rating: getDwellRating(dwellTimeMs), is_pogo: isPogo,
            is_good_abandonment: isGoodAbandonment, exit_to_google: false, scroll_depth_reached: state.maxScrollDepth, had_outbound_click: state.hasOutboundClick,
            cta_clicks: state.ctaClicks, outbound_clicks: state.outboundClicks, affiliate_clicks: state.affiliateClicks,
            time_to_first_cta: state.firstCtaClickTime ? Math.round((state.firstCtaClickTime - state.landingTimestamp) / 1000) : null, conversions: state.conversions.length
        });
        log('Session ended:', { dwellTimeSeconds, isPogo, isGoodAbandonment });
    }

    function initScrollTracking() {
        let ticking = false;
        function onScroll() {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const currentDepth = getScrollDepthPercent(); if (currentDepth > state.maxScrollDepth) state.maxScrollDepth = currentDepth;
                    CONFIG.SCROLL_MILESTONES.forEach(milestone => {
                        if (currentDepth >= milestone && !state.scrollMilestonesReached.has(milestone)) {
                            state.scrollMilestonesReached.add(milestone);
                            trackEvent('navboost:scroll_zone', { scroll_depth_percent: milestone, scroll_zone: CONFIG.SCROLL_ZONES[milestone], time_to_scroll: Math.round((Date.now() - state.landingTimestamp) / 1000) });
                        }
                    });
                    ticking = false;
                });
                ticking = true;
            }
        }
        window.addEventListener('scroll', onScroll, { passive: true }); onScroll(); log('Scroll tracking initialized');
    }

    function initCTATracking() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target; const ctaId = el.dataset.ctaId || el.textContent.substring(0, 30).trim();
                    if (!state.ctasVisible.has(ctaId)) {
                        state.ctasVisible.add(ctaId);
                        trackEvent('navboost:cta_visible', { cta_id: ctaId, cta_type: el.tagName.toLowerCase(), cta_text: el.textContent.substring(0, 50).trim(), time_to_visibility: Math.round((Date.now() - state.landingTimestamp) / 1000) });
                    }
                }
            });
        }, { threshold: 0.5 });
        CONFIG.CTA_SELECTORS.forEach(selector => { try { document.querySelectorAll(selector).forEach(el => observer.observe(el)); } catch (e) {} });
        document.addEventListener('click', (e) => {
            const target = e.target.closest(CONFIG.CTA_SELECTORS.join(','));
            if (target) {
                state.ctaClicks++; if (!state.firstCtaClickTime) state.firstCtaClickTime = Date.now();
                trackEvent('navboost:cta_click', { cta_text: target.textContent.substring(0, 50).trim(), cta_type: target.tagName.toLowerCase(), cta_href: target.href || null, time_to_click: Math.round((Date.now() - state.landingTimestamp) / 1000), was_visible: state.ctasVisible.has(target.dataset.ctaId || target.textContent.substring(0, 30).trim()) });
            }
        });
        log('CTA tracking initialized');
    }

    function initOutboundTracking() {
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]'); if (!link) return;
            const href = link.href; if (!isOutboundLink(href)) return;
            state.outboundClicks++; state.hasOutboundClick = true;
            if (isAffiliateLink(href) || link.rel?.includes('sponsored')) state.affiliateClicks++;
            const outboundDomain = (() => { try { return new URL(href).hostname; } catch { return 'unknown'; } })();
            trackEvent('navboost:outbound_click', { outbound_url: href, outbound_domain: outboundDomain, is_affiliate: isAffiliateLink(href), link_text: link.textContent.substring(0, 50).trim(), time_to_click: Math.round((Date.now() - state.landingTimestamp) / 1000) });
        });
        log('Outbound tracking initialized');
    }

    function initConversionTracking() {
        CONFIG.CONVERSION_FORMS.newsletter.forEach(selector => {
            document.querySelectorAll(selector).forEach(form => {
                form.addEventListener('submit', () => {
                    state.conversions.push('newsletter');
                    trackEvent('conversion:newsletter_signup', { conversion_type: 'newsletter', time_to_convert: Math.round((Date.now() - state.landingTimestamp) / 1000) });
                    if (typeof posthog !== 'undefined') posthog.capture('$conversion', { conversion_type: 'newsletter_signup', value: 1 });
                });
            });
        });
        CONFIG.CONVERSION_FORMS.contact.forEach(selector => {
            document.querySelectorAll(selector).forEach(form => {
                form.addEventListener('submit', () => {
                    state.conversions.push('contact');
                    trackEvent('conversion:contact_form', { conversion_type: 'contact', time_to_convert: Math.round((Date.now() - state.landingTimestamp) / 1000) });
                    if (typeof posthog !== 'undefined') posthog.capture('$conversion', { conversion_type: 'contact_form', value: 1 });
                });
            });
        });
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]'); if (!link) return;
            if (isAffiliateLink(link.href) || link.rel?.includes('sponsored')) {
                state.conversions.push('affiliate');
                trackEvent('conversion:affiliate_click', { conversion_type: 'affiliate', destination_url: link.href, time_to_convert: Math.round((Date.now() - state.landingTimestamp) / 1000) });
                if (typeof posthog !== 'undefined') posthog.capture('$conversion', { conversion_type: 'affiliate_click', value: 1 });
            }
            if (link.href.match(/twitter\.com\/intent|facebook\.com\/sharer|linkedin\.com\/share/i)) {
                state.conversions.push('social_share');
                trackEvent('conversion:social_share', { conversion_type: 'social_share', time_to_share: Math.round((Date.now() - state.landingTimestamp) / 1000) });
            }
        });
        let contentConsumed = false;
        window.addEventListener('scroll', () => {
            if (!contentConsumed && state.maxScrollDepth >= 90) {
                contentConsumed = true; state.conversions.push('content_consumed');
                trackEvent('conversion:content_consumed', { conversion_type: 'content_consumed', scroll_depth: state.maxScrollDepth, time_to_consume: Math.round((Date.now() - state.landingTimestamp) / 1000) });
            }
        }, { passive: true });
        log('Conversion tracking initialized');
    }

    function init() {
        if (typeof posthog === 'undefined') { log('Waiting for PostHog...'); setTimeout(init, 100); return; }
        log('Initializing NavBoost Tracker for northeasttimes.com');
        startSession(); initScrollTracking(); initCTATracking(); initOutboundTracking(); initConversionTracking();
        window.addEventListener('beforeunload', endSession); window.addEventListener('pagehide', endSession);
        document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') endSession(); });
        log('NavBoost Tracker fully initialized');
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
