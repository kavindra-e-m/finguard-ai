package com.finguard.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

/**
 * Response DTO for expense summary.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExpenseSummaryResponse {
    
    private BigDecimal totalThisMonth;
    private BigDecimal totalLastMonth;
    private String topCategory;
    private List<CategoryBreakdown> categoryBreakdown;
    private Double monthOverMonthChange;
    
    /**
     * Category breakdown item.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class CategoryBreakdown {
        private String category;
        private BigDecimal amount;
        private Double percentage;
    }
}
