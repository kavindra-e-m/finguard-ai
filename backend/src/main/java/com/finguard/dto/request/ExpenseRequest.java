package com.finguard.dto.request;

import com.finguard.model.Expense.ExpenseCategory;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Request DTO for creating an expense.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ExpenseRequest {
    
    @NotNull(message = "Category is required")
    private ExpenseCategory category;
    
    @NotNull(message = "Amount is required")
    @Positive(message = "Amount must be positive")
    private BigDecimal amount;
    
    private String description;
    
    @NotNull(message = "Expense date is required")
    private LocalDate expenseDate;
}
