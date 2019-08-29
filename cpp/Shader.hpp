#pragma once

#ifndef SHADER_H
#define SHADER_H

#include <string>

#include <glad/glad.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>

// Simple shader class from http://www.learnopengl.com/ with a few tweaks
class Shader {
public:
	// State
	GLuint ID;

	// Constructor
	Shader(const GLchar *vertexSource, const GLchar *fragmentSource, const GLchar *geometrySource = nullptr, const GLchar *tessCPath = nullptr, const GLchar *tessEPath = nullptr);

	// Sets the current shader as active, do we need to return?
	Shader& use();

	// Not sure compile should be it's own step separate from constructor
	void compile();

	void setFloat(const std::string &name, GLfloat value);
	void setFloat(const GLchar *name, GLfloat value);
	void setInteger(const GLchar *name, GLint value);

	void setVector2f(const GLchar *name, GLfloat x, GLfloat y);
	void setVector2f(const GLchar *name, const glm::vec2 &value);

	void setVector3f(const GLchar *name, GLfloat x, GLfloat y, GLfloat z);
	void setVector3f(const GLchar *name, const glm::vec3 &value);
	void setVector3f(const std::string &name, GLfloat x, GLfloat y, GLfloat z);
	void setVector3f(const  std::string &name, const glm::vec3 &value);

	void setVector4f(const GLchar *name, GLfloat x, GLfloat y, GLfloat z, GLfloat w);
	void setVector4f(const GLchar *name, const glm::vec4 &value);

	void setMatrix4(const GLchar *name, const glm::mat4 &matrix);
private:
	// Checks if compilation or linking failed and if so, print the error logs
	void checkCompileErrors(const GLuint &object, std::string type);

	// Make a shader from a filepath
	GLuint pathToShader(const GLchar * path, GLenum shaderType);

	// Get a string of the shader type from the GLenum
	std::string shaderTypeToString(GLenum shaderType);

	const GLchar* mVertexPath;
	const GLchar* mFragmentPath;
	const GLchar* mGeometryPath;
	const GLchar* mTessCPath;
	const GLchar* mTessEPath;
};

#endif