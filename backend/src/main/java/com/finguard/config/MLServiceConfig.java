package com.finguard.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

/**
 * Configuration for ML service integration.
 */
@Configuration
public class MLServiceConfig {
    
    @Value("${ml.service.url:http://localhost:8000}")
    private String mlServiceUrl;
    
    /**
     * RestTemplate for calling ML service.
     *
     * @return RestTemplate
     */
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    /**
     * Get ML service base URL.
     *
     * @return ML service URL
     */
    public String getMlServiceUrl() {
        return mlServiceUrl;
    }
}
