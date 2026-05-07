package com.finguard.controller;

import com.finguard.dto.request.ExpenseRequest;
import com.finguard.dto.response.AnalyticsResponse;
import com.finguard.dto.response.ExpenseResponse;
import com.finguard.dto.response.ExpenseSummaryResponse;
import com.finguard.security.UserPrincipal;
import com.finguard.service.ExpenseService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * Controller for expense operations.
 */
@RestController
@RequestMapping("/api/expenses")
@RequiredArgsConstructor
@SecurityRequirement(name = "bearerAuth")
@Tag(name = "Expenses", description = "Expense management endpoints")
public class ExpenseController {
    
    private final ExpenseService expenseService;
    
    /**
     * Create a new expense.
     *
     * @param userPrincipal authenticated user
     * @param request expense request
     * @return created expense
     */
    @PostMapping
    @Operation(summary = "Create expense", description = "Add a new expense record")
    public ResponseEntity<ExpenseResponse> createExpense(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @Valid @RequestBody ExpenseRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(expenseService.createExpense(userPrincipal.getId(), request));
    }
    
    /**
     * Get all expenses for the authenticated user.
     *
     * @param userPrincipal authenticated user
     * @param pageable pagination info
     * @return page of expenses
     */
    @GetMapping
    @Operation(summary = "Get expenses", description = "Get paginated list of user expenses")
    public ResponseEntity<Page<ExpenseResponse>> getExpenses(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PageableDefault(size = 20) Pageable pageable) {
        return ResponseEntity.ok(expenseService.getUserExpenses(userPrincipal.getId(), pageable));
    }
    
    /**
     * Get expense summary.
     *
     * @param userPrincipal authenticated user
     * @return expense summary
     */
    @GetMapping("/summary")
    @Operation(summary = "Get expense summary", description = "Get expense summary statistics")
    public ResponseEntity<ExpenseSummaryResponse> getSummary(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(expenseService.getExpenseSummary(userPrincipal.getId()));
    }
    
    /**
     * Get monthly trend data.
     *
     * @param userPrincipal authenticated user
     * @return monthly trend
     */
    @GetMapping("/monthly-trend")
    @Operation(summary = "Get monthly trend", description = "Get monthly expense trend for last 12 months")
    public ResponseEntity<List<AnalyticsResponse.MonthlyTrend>> getMonthlyTrend(
            @AuthenticationPrincipal UserPrincipal userPrincipal) {
        return ResponseEntity.ok(expenseService.getMonthlyTrend(userPrincipal.getId(), 12));
    }
    
    /**
     * Delete an expense.
     *
     * @param userPrincipal authenticated user
     * @param id expense ID
     * @return no content
     */
    @DeleteMapping("/{id}")
    @Operation(summary = "Delete expense", description = "Delete an expense record")
    public ResponseEntity<Void> deleteExpense(
            @AuthenticationPrincipal UserPrincipal userPrincipal,
            @PathVariable Long id) {
        expenseService.deleteExpense(userPrincipal.getId(), id);
        return ResponseEntity.noContent().build();
    }
}
