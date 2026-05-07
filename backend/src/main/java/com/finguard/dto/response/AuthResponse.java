package com.finguard.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for authentication operations.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AuthResponse {
    
    private String token;
    private UserInfo user;
    
    /**
     * Nested user info class.
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class UserInfo {
        private Long id;
        private String name;
        private String email;
        private String monthlyIncome;
    }
}
