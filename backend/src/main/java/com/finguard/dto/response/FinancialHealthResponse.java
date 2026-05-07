package com.finguard.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

/**
 * Response DTO for financial health assessment.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FinancialHealthResponse {
    
    private Integer overallScore;
    private String grade;
    private Map<String, Integer> breakdown;
    private List<String> recommendations;
    private List<String> riskFactors;
}
