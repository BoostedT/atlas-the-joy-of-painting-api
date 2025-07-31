# Database Design: The Joy of Painting API

## Overview

This document outlines the database design for the ETL project "The Joy of Painting API." The database consolidates data from various formats to allow filtering episodes based on original broadcast date, colors used, and subject matter.

## Entities and Relationships (UML Overview)

**Tables:**

### 1. episodes

* `id` (Primary Key)
* `title` (string)
* `season` (integer)
* `episode` (integer)
* `air_date` (date)
* `image_url` (text)
* `video_url` (text)

### 2. colors

* `id` (Primary Key)
* `name` (string, unique)
* `hex_code` (string)

### 3. subjects

* `id` (Primary Key)
* `name` (string, unique)

### 4. episode\_colors (join table)

* `episode_id` (Foreign Key to episodes.id)
* `color_id` (Foreign Key to colors.id)
* **Primary Key:** (`episode_id`, `color_id`)

### 5. episode\_subjects (join table)

* `episode_id` (Foreign Key to episodes.id)
* `subject_id` (Foreign Key to subjects.id)
* **Primary Key:** (`episode_id`, `subject_id`)

## UML Diagram (Text Version)

```
[episodes]             [colors]              [subjects]
  id (PK)                id (PK)               id (PK)
  title                  name                  name
  season                 hex_code
  episode
  air_date
  image_url
  video_url

    |                         |                       |
    |                         |                       |
    |                         |                       |
[episode_colors]       [episode_subjects]
  episode_id (FK)        episode_id (FK)
  color_id (FK)          subject_id (FK)
```

## Rationale

* Normalized many-to-many relationships for both colors and subjects so each can appear in multiple episodes.
* Included `air_date` to enable filtering episodes by broadcast **month**.
* Primary key constraints ensure uniqueness in join tables.

## Tech

* Compatible with PostgreSQL (default) or MySQL with minor changes.
* Table names and relationships optimized for fast lookup and filtering for the API frontend.
