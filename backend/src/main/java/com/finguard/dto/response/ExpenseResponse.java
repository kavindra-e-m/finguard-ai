package com.finguard.dto.response;

import com.finguard.model.Expense.ExpenseCategory;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Response DTO for expense data.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ExpenseResponse {
    
    private Long id;
    private ExpenseCategory category;
    private BigDecimal amount;
    private String description;
    private LocalDate expenseDate;
    private String createdAt;
    private Boolean isAnomaly;
}
