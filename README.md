
# Python Systems Projects

This repository contains a collection of Python systems developed as part of my coursework for **INFO1110 (Introduction to Programming)** at the University of Sydney. The project focuses on object‑oriented design, recursion, decorators, and system‑level thinking.

---

## Key Features

### Gravity-Based Connect Four

A custom implementation of Connect Four with extended mechanics and system architecture.

#### **Object-Oriented Architecture**
- `Game`, `Board`, `Player`, and `Piece` classes  
- Inheritance for special pieces (`BombPiece`, `TeleportPiece`)

#### **Decorator Pattern**
- `@gravity_decorator` dynamically applies gravity effects after piece insertion  

#### **Special Pieces**
- **BombPiece**: Clears a 3×3 area on impact  
- **TeleportPiece**: Swaps position with the mirrored board location  

#### **Win Detection System**
- Horizontal, vertical, and diagonal checks supporting multiple players

#### **State Management**
- Piece inventories  
- Turn switching  
- Draw detection  

---

## Recursive Story & Shape Generator

This module includes:

- Recursive **dungeon storytelling** system  
- **Grammar-based** random sentence generator  
- Recursive ASCII **shape rendering** (stairs, squares, diamonds)  
- String reversal using recursion  

---

## Fitness Tracking System

A file‑based fitness tracking system featuring:

- User login & data persistence  
- Distance and duration analytics  
- Monthly and all-time statistics  
- Goal‑based health planning (marathon, ironman, speed goals)  
- Unit conversion (miles ↔ kilometers)

---

## Methods

- Object‑Oriented programming (OOP)  
- Inheritance 
- Python decorators  
- Recursion  
- File I/O  
- Input validation  
- Game state management  
