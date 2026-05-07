package com.finguard.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/**
 * Response DTOs for portfolio operations.
 */
public class PortfolioResponse {
    
    /**
     * Portfolio optimization response.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Optimization {
        private Map<String, Double> weights;
        private Map<String, BigDecimal> allocationAmounts;
        private Double expectedAnnualReturn;
        private Double annualVolatility;
        private Double sharpeRatio;
        private String riskLabel;
    }
    
    /**
     * Investment response.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Investment {
        private Long id;
        private String investmentType;
        private BigDecimal amount;
        private Double expectedReturn;
        private LocalDate investmentDate;
    }
    
    /**
     * Portfolio summary response.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class Summary {
        private BigDecimal totalInvested;
        private BigDecimal totalCurrentValue;
        private BigDecimal totalReturn;
        private Double returnPercentage;
        private Map<String, BigDecimal> assetAllocation;
        private List<Investment> investments;
    }
}
