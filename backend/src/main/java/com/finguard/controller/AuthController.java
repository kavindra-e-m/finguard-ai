package com.finguard.controller;

import com.finguard.dto.request.LoginRequest;
import com.finguard.dto.request.RegisterRequest;
import com.finguard.dto.response.AuthResponse;
import com.finguard.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Controller for authentication operations.
 */
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@Tag(name = "Authentication", description = "Authentication endpoints")
public class AuthController {
    
    private final AuthService authService;
    
    /**
     * Register a new user.
     *
     * @param request registration request
     * @return authentication response
     */
    @PostMapping("/register")
    @Operation(summary = "Register a new user", description = "Create a new user account")
    public ResponseEntity<AuthResponse> register(@Valid @RequestBody RegisterRequest request) {
        return ResponseEntity.ok(authService.register(request));
    }
    
    /**
     * Login user.
     *
     * @param request login request
     * @return authentication response
     */
    @PostMapping("/login")
    @Operation(summary = "User login", description = "Authenticate user and return JWT token")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }
}
