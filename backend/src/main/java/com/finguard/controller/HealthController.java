package com.finguard.controller;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * Health check controller.
 */
@RestController
@RequestMapping("/api/health")
@Tag(name = "Health", description = "Health check endpoints")
public class HealthController {
    
    /**
     * Health check endpoint.
     *
     * @return health status
     */
    @GetMapping
    @Operation(summary = "Health check", description = "Check if service is running")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "UP");
        response.put("service", "finguard-backend");
        response.put("timestamp", LocalDateTime.now().toString());
        return ResponseEntity.ok(response);
    }
}
