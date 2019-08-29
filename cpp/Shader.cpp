#include "Shader.hpp"

#include <fstream>
#include <sstream>

#include <iostream>

Shader::Shader(const GLchar *vertexPath, const GLchar *fragmentPath, const GLchar *geometryPath, const GLchar *tessCPath, const GLchar *tessEPath) {
	mVertexPath = vertexPath;
	mFragmentPath = fragmentPath;
	mGeometryPath = geometryPath;
	mTessCPath = tessCPath;
	mTessEPath = tessEPath;
}

Shader &Shader::use() {
	glUseProgram(ID);
	return *this;
}

void Shader::compile() {

	GLuint vertexShader = pathToShader(mVertexPath, GL_VERTEX_SHADER);
	GLuint fragmentShader = pathToShader(mFragmentPath, GL_FRAGMENT_SHADER);
	GLuint geometryShader = (mGeometryPath)? pathToShader(mGeometryPath, GL_GEOMETRY_SHADER) : 0;
	GLuint tessCShader = (mTessCPath) ? pathToShader(mTessCPath, GL_TESS_CONTROL_SHADER) : 0;
	GLuint tessEShader = (mTessEPath) ? pathToShader(mTessEPath, GL_TESS_EVALUATION_SHADER) : 0;

	// Create Program
	ID = glCreateProgram();
	
	// Attach the shaders to the program
	glAttachShader(ID, vertexShader);
	glAttachShader(ID, fragmentShader);
	if (mGeometryPath) glAttachShader(ID, geometryShader);
	if (mTessCPath) glAttachShader(ID, tessCShader);
	if (mTessEPath) glAttachShader(ID, tessEShader);

	glLinkProgram(ID);
	checkCompileErrors(ID, "Program");

	// Delete the shaders as they're linked into our program now and no longer necessery
	glDeleteShader(vertexShader);
	glDeleteShader(fragmentShader);
	if (mGeometryPath) glDeleteShader(geometryShader);
	if (mTessCPath) glDeleteShader(tessCShader);
	if (mTessEPath) glDeleteShader(tessEShader);
}

void Shader::setFloat(const std::string &name, GLfloat value) {
	glUniform1f(glGetUniformLocation(ID, name.c_str()), value);
}
void Shader::setFloat(const GLchar *name, GLfloat value) {
	glUniform1f(glGetUniformLocation(ID, name), value);
}
void Shader::setInteger(const GLchar *name, GLint value) {
	glUniform1i(glGetUniformLocation(ID, name), value);
}
void Shader::setVector2f(const GLchar *name, GLfloat x, GLfloat y) {
	glUniform2f(glGetUniformLocation(ID, name), x, y);
}
void Shader::setVector2f(const GLchar *name, const glm::vec2 &value) {
	glUniform2f(glGetUniformLocation(ID, name), value.x, value.y);
}
void Shader::setVector3f(const GLchar *name, GLfloat x, GLfloat y, GLfloat z) {
	glUniform3f(glGetUniformLocation(ID, name), x, y, z);
}
void Shader::setVector3f(const GLchar *name, const glm::vec3 &value) {
	glUniform3f(glGetUniformLocation(ID, name), value.x, value.y, value.z);
}
void Shader::setVector3f(const std::string &name, GLfloat x, GLfloat y, GLfloat z) {
	glUniform3f(glGetUniformLocation(ID, name.c_str()), x, y, z);
}
void Shader::setVector3f(const std::string &name, const glm::vec3 &value) {
	glUniform3fv(glGetUniformLocation(ID, name.c_str()), 1, &value[0]);
}
void Shader::setVector4f(const GLchar *name, GLfloat x, GLfloat y, GLfloat z, GLfloat w) {
	glUniform4f(glGetUniformLocation(ID, name), x, y, z, w);
}
void Shader::setVector4f(const GLchar *name, const glm::vec4 &value) {
	glUniform4f(glGetUniformLocation(ID, name), value.x, value.y, value.z, value.w);
}
void Shader::setMatrix4(const GLchar *name, const glm::mat4 &matrix) {
	glUniformMatrix4fv(glGetUniformLocation(ID, name), 1, GL_FALSE, glm::value_ptr(matrix));
}

void Shader::checkCompileErrors(const GLuint &object, std::string type) {
	GLint success;
	GLchar infoLog[1024];
	
	if (type != "Program") {
		glGetShaderiv(object, GL_COMPILE_STATUS, &success);
		if (!success) {
			glGetShaderInfoLog(object, 1024, NULL, infoLog);
			std::cout << "| ERROR::SHADER: Compile-time error: Type: " << type << std::endl;
			std::cout << infoLog << "\n -- --------------------------------------------------- -- \n";
		}
	} else {
		glGetProgramiv(object, GL_LINK_STATUS, &success);
		if (!success) {
			glGetProgramInfoLog(object, 1024, NULL, infoLog);
			std::cout << "| ERROR::Shader: Link-time error: Type: " << type << std::endl;
			std::cout << infoLog << "\n -- --------------------------------------------------- -- \n";
		}
	}
}

GLuint Shader::pathToShader(const GLchar* path, GLenum shaderType) {
	std::ifstream shaderFile;
	std::stringstream shaderStream;

	shaderFile.open(path);
	shaderStream << shaderFile.rdbuf();
	shaderFile.close();

	std::string code = shaderStream.str();
	const GLchar * ccode = code.c_str();

	// Vertex Shader
	GLuint shader;
	shader = glCreateShader(shaderType);
	glShaderSource(shader, 1, &ccode, NULL);
	glCompileShader(shader);
	checkCompileErrors(shader, shaderTypeToString(shaderType));

	return shader;
}

std::string Shader::shaderTypeToString(GLenum shaderType) {
	std::string ret = "";

	switch (shaderType) {
	case GL_COMPUTE_SHADER:
		ret = "Compute";
		break;
	case GL_VERTEX_SHADER:
		ret = "Vertex";
		break;
	case GL_TESS_CONTROL_SHADER:
		ret = "Tessellation Control";
		break;
	case GL_TESS_EVALUATION_SHADER:
		ret = "Tessellation Evaluation";
		break;
	case GL_GEOMETRY_SHADER:
		ret = "Geometry";
		break;
	case GL_FRAGMENT_SHADER:
		ret = "Fragment";
		break;
	default:
		ret = "unknown";
		break;
	}
	return ret;
}
