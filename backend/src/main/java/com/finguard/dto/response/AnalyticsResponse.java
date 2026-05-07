package com.finguard.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

/**
 * Response DTOs for analytics endpoints.
 */
public class AnalyticsResponse {
    
    /**
     * Monthly trend data point.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MonthlyTrend {
        private String month;
        private BigDecimal total;
    }
    
    /**
     * Expense prediction response.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ExpensePrediction {
        private BigDecimal predictedNextMonth;
        private BigDecimal confidenceLower;
        private BigDecimal confidenceUpper;
        private String trend;
        private List<BigDecimal> forecast3Months;
    }
    
    /**
     * Personality detection response.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class PersonalityDetection {
        private String personalityType;
        private Double confidence;
        private Map<String, Double> probabilities;
        private String description;
    }
    
    /**
     * Stress prediction response.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class StressPrediction {
        private Double riskScore;
        private String riskLabel;
        private List<String> alerts;
        private List<String> recommendations;
    }
    
    /**
     * Anomaly detection response.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class AnomalyDetection {
        private List<AnomalyItem> anomalies;
        private Integer totalAnomalies;
        private Integer totalTransactions;
    }
    
    /**
     * Anomaly item.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class AnomalyItem {
        private Long expenseId;
        private BigDecimal amount;
        private String category;
        private Double anomalyScore;
        private String reason;
    }
}
