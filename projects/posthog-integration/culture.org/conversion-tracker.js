/**
 * Enhanced Conversion Tracker - culture.org
 *
 * Tracks 5 conversion types:
 * 1. Newsletter Signup
 * 2. Ad Clicks
 * 3. Affiliate Clicks
 * 4. Article Completion
 * 5. Return Visits
 *
 * PostHog Project ID: 295222
 * Generated: 2026-01-21
 */

(function() {
    'use strict';

    // ==========================================
    // CONFIGURATION
    // ==========================================
    const CONVERSION_CONFIG = {
        SITE_DOMAIN: 'culture.org',

        // Newsletter form selectors (WordPress common patterns)
        NEWSLETTER_SELECTORS: [
            // Mailchimp
            'form[action*="mailchimp"]',
            'form[action*="list-manage"]',
            '.mc4wp-form',
            '#mc-embedded-subscribe-form',
            // Generic newsletter
            'form[action*="newsletter"]',
            'form[action*="subscribe"]',
            '.newsletter-form',
            '.subscribe-form',
            '.email-signup-form',
            '#newsletter-form',
            '#subscribe-form',
            // Input-based detection
            'form:has(input[name*="email"]):has(button:contains("Subscribe"))',
            'form:has(input[placeholder*="email"]):has(button[type="submit"])',
            // WordPress plugins
            '.jetpack-subscribe-modal form',
            '.wp-block-jetpack-subscriptions form',
            '.nf-form-cont', // Ninja Forms
            '.wpforms-form', // WPForms
            '.gform_wrapper form', // Gravity Forms
        ],

        // Ad network selectors
        AD_SELECTORS: [
            // Google Ads
            'ins.adsbygoogle',
            '[data-ad-client]',
            'iframe[src*="googlesyndication"]',
            'iframe[src*="doubleclick"]',
            // Generic ad containers
            '.advertisement',
            '.ad-container',
            '.ad-wrapper',
            '.ad-unit',
            '[class*="ad-"]',
            '[id*="ad-"]',
            '[data-ad]',
            // Specific ad networks
            'iframe[src*="taboola"]',
            'iframe[src*="outbrain"]',
            '.trc_related_container', // Taboola
            '.OUTBRAIN', // Outbrain
            // Sponsored content
            '.sponsored-content a',
            '.native-ad a',
        ],

        // Affiliate link patterns
        AFFILIATE_PATTERNS: [
            // URL patterns
            /\/go\//i,
            /\/out\//i,
            /\/aff\//i,
            /\/partner\//i,
            /\/redirect\//i,
            /\/visit\//i,
            /\/click\//i,
            /\?ref=/i,
            /\?aff=/i,
            /\?affiliate/i,
            /\?tag=/i,
            /\?utm_campaign=affiliate/i,
            // Known affiliate networks
            /amazon\.com.*tag=/i,
            /shareasale\.com/i,
            /cj\.com|commission-junction/i,
            /rakuten\.com/i,
            /awin\.com/i,
            /partnerize\.com/i,
            // Gambling/Betting affiliates (seen in hudsonreporter)
            /bet365|draftkings|fanduel|betmgm|caesars|pointsbet/i,
            /sportsbook|betting|casino/i,
        ],

        // Article completion thresholds
        ARTICLE_COMPLETION: {
            STARTED: 25,      // Started reading
            ENGAGED: 50,      // Engaged with content
            CONSUMED: 75,     // Consumed most content
            COMPLETED: 90,    // Completed article
        },

        // Return visit tracking
        RETURN_VISIT: {
            STORAGE_KEY: 'nb_visitor_data',
            NEW_VISIT_THRESHOLD_HOURS: 24,
        },

        DEBUG: true
    };

    // ==========================================
    // STATE
    // ==========================================
    const conversionState = {
        sessionStart: Date.now(),
        conversions: [],
        newsletterFormsFound: 0,
        adsFound: 0,
        affiliateLinksFound: 0,
        articleScrollMilestones: new Set(),
        isReturningVisitor: false,
        visitCount: 0,
        lastVisit: null,
    };

    // ==========================================
    // UTILITIES
    // ==========================================
    function log(...args) {
        if (CONVERSION_CONFIG.DEBUG) {
            console.log('[ConversionTracker]', ...args);
        }
    }

    function trackConversion(type, properties = {}) {
        if (typeof posthog === 'undefined') {
            log('PostHog not available');
            return;
        }

        const baseProps = {
            conversion_type: type,
            time_to_conversion: Math.round((Date.now() - conversionState.sessionStart) / 1000),
            page_url: window.location.href,
            page_path: window.location.pathname,
            is_returning_visitor: conversionState.isReturningVisitor,
            visit_count: conversionState.visitCount,
        };

        // Track specific conversion event
        posthog.capture(`conversion:${type}`, { ...baseProps, ...properties });

        // Track generic conversion for funnel analysis
        posthog.capture('$conversion', {
            conversion_type: type,
            value: properties.value || 1,
            ...properties
        });

        conversionState.conversions.push(type);
        log(`Conversion tracked: ${type}`, properties);
    }

    // ==========================================
    // 1. NEWSLETTER SIGNUP TRACKING
    // ==========================================
    function initNewsletterTracking() {
        let formsFound = 0;

        // Method 1: Direct form selectors
        CONVERSION_CONFIG.NEWSLETTER_SELECTORS.forEach(selector => {
            try {
                document.querySelectorAll(selector).forEach(form => {
                    if (form.dataset.conversionTracked) return;
                    form.dataset.conversionTracked = 'true';
                    formsFound++;

                    form.addEventListener('submit', (e) => {
                        const emailInput = form.querySelector('input[type="email"], input[name*="email"]');
                        const email = emailInput ? emailInput.value : null;

                        trackConversion('newsletter_signup', {
                            form_id: form.id || null,
                            form_action: form.action || null,
                            has_email: !!email,
                            form_selector: selector,
                            value: 5, // Newsletter signup value
                        });
                    });
                });
            } catch (e) { /* Invalid selector */ }
        });

        // Method 2: Monitor for dynamically added forms
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) {
                        const forms = node.querySelectorAll ?
                            node.querySelectorAll('form') : [];
                        forms.forEach(form => {
                            if (isNewsletterForm(form) && !form.dataset.conversionTracked) {
                                form.dataset.conversionTracked = 'true';
                                formsFound++;
                                form.addEventListener('submit', () => {
                                    trackConversion('newsletter_signup', {
                                        form_id: form.id || null,
                                        dynamic: true,
                                        value: 5,
                                    });
                                });
                            }
                        });
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });

        // Method 3: Track email input focus + button clicks as intent
        document.querySelectorAll('input[type="email"]').forEach(input => {
            let focused = false;
            input.addEventListener('focus', () => {
                if (!focused) {
                    focused = true;
                    posthog.capture('newsletter:email_focus', {
                        input_placeholder: input.placeholder,
                        form_id: input.form?.id || null,
                    });
                }
            });
        });

        conversionState.newsletterFormsFound = formsFound;
        log(`Newsletter tracking initialized. Forms found: ${formsFound}`);
    }

    function isNewsletterForm(form) {
        const action = (form.action || '').toLowerCase();
        const classes = (form.className || '').toLowerCase();
        const id = (form.id || '').toLowerCase();

        const keywords = ['newsletter', 'subscribe', 'mailchimp', 'email-signup', 'list-manage'];
        return keywords.some(kw =>
            action.includes(kw) || classes.includes(kw) || id.includes(kw)
        ) || form.querySelector('input[type="email"]');
    }

    // ==========================================
    // 2. AD CLICK TRACKING
    // ==========================================
    function initAdTracking() {
        let adsFound = 0;

        // Track ad visibility
        const adObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const ad = entry.target;
                    if (!ad.dataset.adViewed) {
                        ad.dataset.adViewed = 'true';
                        posthog.capture('ad:impression', {
                            ad_position: getAdPosition(ad),
                            ad_type: getAdType(ad),
                            ad_size: `${ad.offsetWidth}x${ad.offsetHeight}`,
                        });
                    }
                }
            });
        }, { threshold: 0.5 });

        // Find and track ads
        CONVERSION_CONFIG.AD_SELECTORS.forEach(selector => {
            try {
                document.querySelectorAll(selector).forEach(ad => {
                    adsFound++;
                    adObserver.observe(ad);

                    // Track clicks on/within ad containers
                    ad.addEventListener('click', (e) => {
                        trackConversion('ad_click', {
                            ad_type: getAdType(ad),
                            ad_position: getAdPosition(ad),
                            ad_size: `${ad.offsetWidth}x${ad.offsetHeight}`,
                            click_target: e.target.tagName,
                            value: 1,
                        });
                    }, true);
                });
            } catch (e) { /* Invalid selector */ }
        });

        // Track clicks on iframes (can't track inside, but can detect click-away)
        document.querySelectorAll('iframe').forEach(iframe => {
            if (isAdIframe(iframe)) {
                adsFound++;

                // Detect when user focuses on iframe (indicates ad interaction)
                window.addEventListener('blur', () => {
                    if (document.activeElement === iframe) {
                        trackConversion('ad_click', {
                            ad_type: 'iframe',
                            ad_src: iframe.src?.substring(0, 100),
                            value: 1,
                        });
                    }
                });
            }
        });

        conversionState.adsFound = adsFound;
        log(`Ad tracking initialized. Ads found: ${adsFound}`);
    }

    function getAdType(element) {
        const src = element.src || '';
        const classes = element.className || '';

        if (src.includes('googlesyndication') || src.includes('doubleclick')) return 'google_ads';
        if (src.includes('taboola') || classes.includes('trc_')) return 'taboola';
        if (src.includes('outbrain') || classes.includes('OUTBRAIN')) return 'outbrain';
        if (classes.includes('sponsored')) return 'sponsored';
        return 'display';
    }

    function getAdPosition(element) {
        const rect = element.getBoundingClientRect();
        const viewportHeight = window.innerHeight;

        if (rect.top < viewportHeight * 0.3) return 'above_fold';
        if (rect.top < viewportHeight * 0.7) return 'mid_content';
        return 'below_fold';
    }

    function isAdIframe(iframe) {
        const src = (iframe.src || '').toLowerCase();
        return /googlesyndication|doubleclick|taboola|outbrain|ad/.test(src);
    }

    // ==========================================
    // 3. AFFILIATE CLICK TRACKING
    // ==========================================
    function initAffiliateTracking() {
        let affiliateLinksFound = 0;

        // Scan all links
        document.querySelectorAll('a[href]').forEach(link => {
            if (isAffiliateLink(link.href)) {
                affiliateLinksFound++;
                link.dataset.affiliateTracked = 'true';

                link.addEventListener('click', (e) => {
                    const destination = getAffiliateDomain(link.href);
                    const category = getAffiliateCategory(link.href);

                    trackConversion('affiliate_click', {
                        affiliate_url: link.href,
                        affiliate_domain: destination,
                        affiliate_category: category,
                        link_text: link.textContent.substring(0, 50).trim(),
                        link_position: getLinkPosition(link),
                        is_sponsored: link.rel?.includes('sponsored') || false,
                        value: category === 'gambling' ? 10 : 3, // Higher value for gambling
                    });
                });
            }
        });

        // Monitor for dynamically added affiliate links
        const observer = new MutationObserver((mutations) => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) {
                        const links = node.querySelectorAll ?
                            node.querySelectorAll('a[href]') : [];
                        links.forEach(link => {
                            if (isAffiliateLink(link.href) && !link.dataset.affiliateTracked) {
                                link.dataset.affiliateTracked = 'true';
                                affiliateLinksFound++;
                                link.addEventListener('click', () => {
                                    trackConversion('affiliate_click', {
                                        affiliate_url: link.href,
                                        affiliate_domain: getAffiliateDomain(link.href),
                                        dynamic: true,
                                        value: 3,
                                    });
                                });
                            }
                        });
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });

        conversionState.affiliateLinksFound = affiliateLinksFound;
        log(`Affiliate tracking initialized. Links found: ${affiliateLinksFound}`);
    }

    function isAffiliateLink(href) {
        if (!href) return false;
        return CONVERSION_CONFIG.AFFILIATE_PATTERNS.some(pattern => pattern.test(href));
    }

    function getAffiliateDomain(href) {
        try {
            return new URL(href).hostname;
        } catch {
            return 'unknown';
        }
    }

    function getAffiliateCategory(href) {
        const lowerHref = href.toLowerCase();
        if (/bet365|draftkings|fanduel|betmgm|caesars|pointsbet|sportsbook|betting|casino/i.test(lowerHref)) {
            return 'gambling';
        }
        if (/amazon/i.test(lowerHref)) return 'ecommerce';
        if (/booking|hotel|expedia|airbnb/i.test(lowerHref)) return 'travel';
        return 'general';
    }

    function getLinkPosition(link) {
        const rect = link.getBoundingClientRect();
        const viewportHeight = window.innerHeight;

        if (rect.top < viewportHeight * 0.3) return 'top';
        if (rect.top < viewportHeight * 0.7) return 'middle';
        return 'bottom';
    }

    // ==========================================
    // 4. ARTICLE COMPLETION TRACKING
    // ==========================================
    function initArticleCompletionTracking() {
        // Only track on article pages
        if (!isArticlePage()) {
            log('Not an article page, skipping article completion tracking');
            return;
        }

        const articleContent = document.querySelector(
            'article, .post-content, .entry-content, .article-content, main article, .single-post'
        );

        if (!articleContent) {
            log('No article content found');
            return;
        }

        // Track time spent reading
        let readingTime = 0;
        let isReading = true;

        const readingInterval = setInterval(() => {
            if (isReading && document.visibilityState === 'visible') {
                readingTime++;
            }
        }, 1000);

        document.addEventListener('visibilitychange', () => {
            isReading = document.visibilityState === 'visible';
        });

        // Track scroll progress through article
        let maxArticleScroll = 0;

        function getArticleScrollPercent() {
            const rect = articleContent.getBoundingClientRect();
            const articleTop = rect.top + window.pageYOffset;
            const articleHeight = articleContent.offsetHeight;
            const viewportHeight = window.innerHeight;
            const scrollTop = window.pageYOffset;

            const scrollIntoArticle = scrollTop - articleTop + viewportHeight;
            const percent = Math.min(100, Math.max(0, (scrollIntoArticle / articleHeight) * 100));

            return Math.round(percent);
        }

        window.addEventListener('scroll', () => {
            const currentPercent = getArticleScrollPercent();

            if (currentPercent > maxArticleScroll) {
                maxArticleScroll = currentPercent;

                // Check milestones
                Object.entries(CONVERSION_CONFIG.ARTICLE_COMPLETION).forEach(([name, threshold]) => {
                    if (currentPercent >= threshold && !conversionState.articleScrollMilestones.has(name)) {
                        conversionState.articleScrollMilestones.add(name);

                        const eventName = `article_${name.toLowerCase()}`;

                        if (name === 'COMPLETED') {
                            // Full conversion for completion
                            trackConversion('article_completion', {
                                article_url: window.location.pathname,
                                article_title: document.title,
                                reading_time_seconds: readingTime,
                                scroll_depth: currentPercent,
                                value: 2,
                            });
                        } else {
                            // Progress event
                            posthog.capture(`article:${eventName}`, {
                                article_url: window.location.pathname,
                                scroll_depth: currentPercent,
                                reading_time_seconds: readingTime,
                            });
                        }

                        log(`Article milestone: ${name} (${threshold}%)`);
                    }
                });
            }
        }, { passive: true });

        // Track on page leave
        window.addEventListener('beforeunload', () => {
            clearInterval(readingInterval);

            posthog.capture('article:session_end', {
                article_url: window.location.pathname,
                final_scroll_depth: maxArticleScroll,
                total_reading_time_seconds: readingTime,
                milestones_reached: Array.from(conversionState.articleScrollMilestones),
                completed: conversionState.articleScrollMilestones.has('COMPLETED'),
            });
        });

        log('Article completion tracking initialized');
    }

    function isArticlePage() {
        const path = window.location.pathname;
        const body = document.body.className;

        // Check URL patterns
        if (path.match(/^\/\d{4}\/\d{2}\/\d{2}\//)) return true;
        if (path.includes('/news/') || path.includes('/article/')) return true;

        // Check body classes
        if (body.includes('single-post') || body.includes('single')) return true;
        if (body.includes('article') || body.includes('post-template')) return true;

        // Check for article element
        if (document.querySelector('article.post, article.single')) return true;

        return false;
    }

    // ==========================================
    // 5. RETURN VISIT TRACKING
    // ==========================================
    function initReturnVisitTracking() {
        const storageKey = CONVERSION_CONFIG.RETURN_VISIT.STORAGE_KEY;
        const thresholdHours = CONVERSION_CONFIG.RETURN_VISIT.NEW_VISIT_THRESHOLD_HOURS;

        let visitorData = {
            firstVisit: Date.now(),
            lastVisit: Date.now(),
            visitCount: 1,
            conversions: [],
            pagesViewed: [],
        };

        // Load existing data
        try {
            const stored = localStorage.getItem(storageKey);
            if (stored) {
                const parsed = JSON.parse(stored);
                const hoursSinceLastVisit = (Date.now() - parsed.lastVisit) / (1000 * 60 * 60);

                if (hoursSinceLastVisit >= thresholdHours) {
                    // This is a return visit
                    visitorData = {
                        ...parsed,
                        lastVisit: Date.now(),
                        visitCount: parsed.visitCount + 1,
                    };

                    conversionState.isReturningVisitor = true;
                    conversionState.visitCount = visitorData.visitCount;
                    conversionState.lastVisit = parsed.lastVisit;

                    // Track return visit conversion
                    trackConversion('return_visit', {
                        visit_number: visitorData.visitCount,
                        days_since_last_visit: Math.round(hoursSinceLastVisit / 24),
                        previous_conversions: parsed.conversions?.length || 0,
                        previous_pages_viewed: parsed.pagesViewed?.length || 0,
                        value: visitorData.visitCount >= 3 ? 3 : 1, // Higher value for loyal visitors
                    });

                    log(`Return visitor detected. Visit #${visitorData.visitCount}`);
                } else {
                    // Same session or recent visit
                    visitorData = {
                        ...parsed,
                        lastVisit: Date.now(),
                    };
                    conversionState.visitCount = visitorData.visitCount;
                }
            }
        } catch (e) {
            log('Error loading visitor data:', e);
        }

        // Track current page
        if (!visitorData.pagesViewed.includes(window.location.pathname)) {
            visitorData.pagesViewed.push(window.location.pathname);
            // Keep only last 50 pages
            if (visitorData.pagesViewed.length > 50) {
                visitorData.pagesViewed = visitorData.pagesViewed.slice(-50);
            }
        }

        // Save updated data
        window.addEventListener('beforeunload', () => {
            // Add any conversions from this session
            visitorData.conversions = [
                ...(visitorData.conversions || []),
                ...conversionState.conversions
            ].slice(-100); // Keep last 100 conversions

            try {
                localStorage.setItem(storageKey, JSON.stringify(visitorData));
            } catch (e) {
                log('Error saving visitor data:', e);
            }
        });

        // Set person properties in PostHog
        if (typeof posthog !== 'undefined') {
            posthog.people.set({
                'visit_count': visitorData.visitCount,
                'first_visit': new Date(visitorData.firstVisit).toISOString(),
                'is_returning_visitor': conversionState.isReturningVisitor,
                'total_conversions': (visitorData.conversions?.length || 0) + conversionState.conversions.length,
            });
        }

        log('Return visit tracking initialized. Returning:', conversionState.isReturningVisitor);
    }

    // ==========================================
    // CONVERSION RATE CALCULATION
    // ==========================================
    function reportConversionMetrics() {
        // This runs on page unload to report session metrics
        window.addEventListener('beforeunload', () => {
            if (typeof posthog === 'undefined') return;

            posthog.capture('conversion:session_summary', {
                total_conversions: conversionState.conversions.length,
                conversion_types: [...new Set(conversionState.conversions)],
                newsletter_forms_available: conversionState.newsletterFormsFound,
                ads_available: conversionState.adsFound,
                affiliate_links_available: conversionState.affiliateLinksFound,
                is_returning_visitor: conversionState.isReturningVisitor,
                visit_number: conversionState.visitCount,
                session_duration_seconds: Math.round((Date.now() - conversionState.sessionStart) / 1000),
            });
        });
    }

    // ==========================================
    // INITIALIZATION
    // ==========================================
    function init() {
        if (typeof posthog === 'undefined') {
            log('Waiting for PostHog...');
            setTimeout(init, 100);
            return;
        }

        log('Initializing Enhanced Conversion Tracker for culture.org');

        // Initialize all 5 conversion trackers
        initReturnVisitTracking();      // 5. Return visits (first, to set visitor state)
        initNewsletterTracking();       // 1. Newsletter signup
        initAdTracking();               // 2. Ad clicks
        initAffiliateTracking();        // 3. Affiliate clicks
        initArticleCompletionTracking();// 4. Article completion
        reportConversionMetrics();      // Summary reporting

        log('Enhanced Conversion Tracker fully initialized');
        log('Tracking summary:', {
            newsletterForms: conversionState.newsletterFormsFound,
            ads: conversionState.adsFound,
            affiliateLinks: conversionState.affiliateLinksFound,
            isReturningVisitor: conversionState.isReturningVisitor,
            visitCount: conversionState.visitCount,
        });
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
