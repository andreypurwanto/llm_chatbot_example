CREATE DATABASE `llm_chatbot_example`;

USE `llm_chatbot_example`;

-- Table: models
CREATE TABLE `models` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` char(50) NOT NULL,
  `class_name` char(50) NOT NULL,
  `description` text,
  `is_active` tinyint(1) NOT NULL,
  `model_arg` json NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

-- Table: conversations
CREATE TABLE `conversations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `model_id` int NOT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `external_id` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `model_id` (`model_id`),
  CONSTRAINT `conversations_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `models` (`id`)
);

-- Table: chats
CREATE TABLE `chats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `conversation_id` int NOT NULL,
  `query` text,
  `remark` json DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `conversation_id` (`conversation_id`),
  CONSTRAINT `chats_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`)
);

-- Table: llm_results
CREATE TABLE `llm_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` int NOT NULL,
  `result_metadata` json DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `chat_id` (`chat_id`),
  CONSTRAINT `llm_results_ibfk_1` FOREIGN KEY (`chat_id`) REFERENCES `chats` (`id`)
);

-- Table: user_reviews
CREATE TABLE `user_reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `conversation_id` int NOT NULL,
  `feedback` text,
  `star` smallint DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `conversation_id` (`conversation_id`),
  CONSTRAINT `user_reviews_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`)
);

-- Insert initial model data
INSERT INTO `models`
(name, class_name, description, is_active, model_arg)
VALUES('gpt4_turbo_rag', 'OpenAIRAG', 'open ai rag v1 with gpt 4 turbo', 1, '{"args": {"model_args": {"model": "gpt-4-turbo", "temperature": 0}, "chroma_path": "data/open_ai_rag_v1"}}');