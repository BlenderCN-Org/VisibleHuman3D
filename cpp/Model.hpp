#pragma once
// Std. Includes
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <map>
#include <vector>

// GL Includes
#include <glad/glad.h> // Contains all the necessery OpenGL includes
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <assimp/Importer.hpp>
#include <assimp/scene.h>
#include <assimp/postprocess.h>

#include "Mesh.hpp"

// includes required for soft body simulation
#include "BulletSoftBody/btSoftRigidDynamicsWorld.h"
#include "BulletSoftBody/btSoftBodyRigidBodyCollisionConfiguration.h"
#include "BulletSoftBody/btSoftBodyHelpers.h"

GLint TextureFromFile(const char* path, std::string directory);
void renderSoftbodyMeshes(btSoftBody* sBody);

class Model 
{
public:
    /*  Functions   */
    // Constructor, expects a filepath to a 3D model.
    Model(GLchar* path)
    {
        this->loadModel(path);
    }

    // Draws the model, and thus all its meshes
    void Draw(Shader shader)
    {
        for(GLuint i = 0; i < this->meshes.size(); i++)
            this->meshes[i].Draw(shader);
    }

	void softBodyDraw(Shader shader, btSoftBodyWorldInfo softBodyWorldInfo)
	{
		btScalar* verti = new btScalar[3 * (this->meshes[0].vertices.size())];
		for (int i = 0; i < this->meshes[0].vertices.size(); i++)
		{
			verti[3 * i] = this->meshes[0].vertices[i].Position.x;
			verti[3 * i + 1] = this->meshes[0].vertices[i].Position.y;
			verti[3 * i + 2] = this->meshes[0].vertices[i].Position.z;
		}

		int* indi = new int[this->meshes[0].indices.size()];
		for (int i = 0; i < this->meshes[0].indices.size(); i++)
		{
			indi[i] = this->meshes[0].indices[i];
		}

		btSoftBody* pSphere = btSoftBodyHelpers::CreateFromTriMesh(softBodyWorldInfo, verti,
			&indi[0],
			int(this->meshes[0].indices.size()) / 3);

		// Data to fill
		std::vector<Mesh> btMeshes;
		std::vector<Vertex> btVertices;
		std::vector<GLuint> btIndices;
		std::vector<Texture> btTextures;

		int numNodes = pSphere->m_nodes.size();
		for (int j = 0; j < this->meshes.size(); j++)
		{
			for (int i = 0; i < numNodes; i++)
			{

			Vertex vertex;
			glm::vec3 vector;
			//Position
			vector.x = pSphere->m_nodes.at(i).m_x[0];
			vector.y = pSphere->m_nodes.at(i).m_x[1];
			vector.z = pSphere->m_nodes.at(i).m_x[2];
			vertex.Position = vector;
			//Normal
			vector.x = pSphere->m_nodes.at(i).m_n[0];
			vector.y = pSphere->m_nodes.at(i).m_n[1];
			vector.z = pSphere->m_nodes.at(i).m_n[2];
			vertex.Normal = vector; //sBody->m_faces.at(i).m_n[0]->m_n

			btVertices.push_back(vertex);

			this->meshes.at(j).vertices.at(i).Position.x = btVertices[i].Position.x;
			this->meshes.at(j).vertices.at(i).Position.y = btVertices[i].Position.y;
			this->meshes.at(j).vertices.at(i).Position.z = btVertices[i].Position.z;

			this->meshes.at(j).vertices.at(i).Normal.x = btVertices[i].Normal.x;
			this->meshes.at(j).vertices.at(i).Normal.y = btVertices[i].Normal.y;
			this->meshes.at(j).vertices.at(i).Normal.z = btVertices[i].Normal.z;
			}

			Mesh mesh = Mesh(btVertices, this->meshes[j].indices, this->meshes[j].textures);
			btMeshes.push_back(mesh);
		}

		meshes = btMeshes;	

		Draw(shader);
		
		// Now wak through each of the mesh's faces (a face is a mesh its triangle) and retrieve the corresponding vertex indices.

		//int numFaces = pSphere->m_faces.size(); 
		//for (GLuint i = 0; i < numFaces; i++)
		//	{
		//
		//		btSoftBody::Face face = pSphere->m_faces.at(i);
		//		// Retrieve all indices of the face and store them in the indices std::vector
		//		for (GLuint j = 0; j < face.m_n[i]->m_leaf;//.mNumIndices; j++)
		//			indices.push_back(face.mIndices[j]);
		//	}

	}
	std::vector<Mesh> getMeshes()
	{
		return this->meshes;
	}

	int getNumMeshes()
	{
		return this->mNumMeshes;
	}

	int getNumFaces()
	{
		return this->mNumFaces;
	}


private:
    /*  Model Data  */
    std::vector<Mesh> meshes;
    std::string directory;
    std::vector<Texture> textures_loaded;	// Stores all the textures loaded so far, optimization to make sure textures aren't loaded more than once.
	int mNumMeshes;
	int mNumFaces;

    /*  Functions   */
    // Loads a model with supported ASSIMP extensions from file and stores the resulting meshes in the meshes vector.
    void loadModel(std::string path)
    {
        // Read file via ASSIMP 
        Assimp::Importer importer;
        const aiScene* scene = importer.ReadFile(path, aiProcess_Triangulate | aiProcess_FlipUVs | aiProcess_CalcTangentSpace);
        // Check for errors
        if(!scene || scene->mFlags == AI_SCENE_FLAGS_INCOMPLETE || !scene->mRootNode) // if is Not Zero
        {
            std::cout << "ERROR::ASSIMP:: " << importer.GetErrorString() << std::endl;
            return;
        }
        // Retrieve the directory path of the filepath
        this->directory = path.substr(0, path.find_last_of('/'));

        // Process ASSIMP's root node recursively
        this->processNode(scene->mRootNode, scene);
    }

    // Processes a node in a recursive fashion. Processes each individual mesh located at the node and repeats this process on its children nodes (if any).
    void processNode(aiNode* node, const aiScene* scene)
    {
		// Process each mesh located at the current node
        for(GLuint i = 0; i < node->mNumMeshes; i++)
        {
			this->mNumMeshes = node->mNumMeshes;
            // The node object only contains indices to index the actual objects in the scene. 
            // The scene contains all the data, node is just to keep stuff organized (like relations between nodes).
            aiMesh* mesh = scene->mMeshes[node->mMeshes[i]]; 
            this->meshes.push_back(this->processMesh(mesh, scene));			
        }
        // After we've processed all of the meshes (if any) we then recursively process each of the children nodes
        for(GLuint i = 0; i < node->mNumChildren; i++)
        {
            this->processNode(node->mChildren[i], scene);
        }

    }

    Mesh processMesh(aiMesh* mesh, const aiScene* scene)
    {
        // Data to fill
        std::vector<Vertex> vertices;
        std::vector<GLuint> indices;
        std::vector<Texture> textures;
		std::vector<Face> faces;

        // Walk through each of the mesh's vertices
        for(GLuint i = 0; i < mesh->mNumVertices; i++)
        {
            Vertex vertex;
            glm::vec3 vector; // We declare a placeholder std::vector since assimp uses its own std::vector class that doesn't directly convert to glm's vec3 class so we transfer the data to this placeholder glm::vec3 first.
            // Positions
            vector.x = mesh->mVertices[i].x;
            vector.y = mesh->mVertices[i].y;
            vector.z = mesh->mVertices[i].z;
            vertex.Position = vector;
            // Normals
            vector.x = mesh->mNormals[i].x;
            vector.y = mesh->mNormals[i].y;
            vector.z = mesh->mNormals[i].z;
            vertex.Normal = vector;
            // Texture Coordinates
            if(mesh->mTextureCoords[0]) // Does the mesh contain texture coordinates?
            {
                glm::vec2 vec;
                // A vertex can contain up to 8 different texture coordinates. We thus make the assumption that we won't 
                // use models where a vertex can have multiple texture coordinates so we always take the first set (0).
                vec.x = mesh->mTextureCoords[0][i].x; 
                vec.y = mesh->mTextureCoords[0][i].y;
                vertex.TexCoords = vec;
            }
            else
                vertex.TexCoords = glm::vec2(0.0f, 0.0f);
			
			// tangent
			vector.x = mesh->mTangents[i].x;
			vector.y = mesh->mTangents[i].y;
			vector.z = mesh->mTangents[i].z;
			vertex.Tangent = vector;
			// bitangent
			vector.x = mesh->mBitangents[i].x;
			vector.y = mesh->mBitangents[i].y;
			vector.z = mesh->mBitangents[i].z;
			vertex.Bitangent = vector; 
			
			vertices.push_back(vertex);
        }
        // Now wak through each of the mesh's faces (a face is a mesh its triangle) and retrieve the corresponding vertex indices.
        for(GLuint i = 0; i < mesh->mNumFaces; i++)
        {
			this->mNumFaces = mesh->mNumFaces;

            aiFace face = mesh->mFaces[i];
            // Retrieve all indices of the face and store them in the indices std::vector
            for(GLuint j = 0; j < face.mNumIndices; j++)
                indices.push_back(face.mIndices[j]);
        }
        // Process materials
        if(mesh->mMaterialIndex >= 0)
        {
            aiMaterial* material = scene->mMaterials[mesh->mMaterialIndex];
            // We assume a convention for sampler names in the shaders. Each diffuse texture should be named
            // as 'texture_diffuseN' where N is a sequential number ranging from 1 to MAX_SAMPLER_NUMBER. 
            // Same applies to other texture as the following list summarizes:
            // Diffuse: texture_diffuseN
            // Specular: texture_specularN
            // Normal: texture_normalN

            // 1. Diffuse std::maps
            std::vector<Texture> diffuseMaps = loadMaterialTextures(material, aiTextureType_DIFFUSE, "texture_diffuse");
            textures.insert(textures.end(), diffuseMaps.begin(), diffuseMaps.end());
            // 2. Specular std::maps
            std::vector<Texture> specularMaps = loadMaterialTextures(material, aiTextureType_SPECULAR, "texture_specular");
            textures.insert(textures.end(), specularMaps.begin(), specularMaps.end());
			// 3. normal maps
			std::vector<Texture> normalMaps = loadMaterialTextures(material, aiTextureType_NORMALS, "texture_normal");
			textures.insert(textures.end(), normalMaps.begin(), normalMaps.end());
			// 4. height maps
			std::vector<Texture> heightMaps = loadMaterialTextures(material, aiTextureType_DISPLACEMENT, "texture_height");
			textures.insert(textures.end(), heightMaps.begin(), heightMaps.end());
			// 5. Gloss maps
			std::vector<Texture> glossMaps = loadMaterialTextures(material, aiTextureType_SHININESS, "texture_gloss");
			textures.insert(textures.end(), glossMaps.begin(), glossMaps.end());
			// 6. Ambient maps
			std::vector<Texture> ambientMaps = loadMaterialTextures(material, aiTextureType_AMBIENT, "texture_ambient");
			textures.insert(textures.end(), ambientMaps.begin(), ambientMaps.end());
		}
        
        // Return a mesh object created from the extracted mesh data
        return Mesh(vertices, indices, textures);
    }

    // Checks all material textures of a given type and loads the textures if they're not loaded yet.
    // The required info is returned as a Texture struct.
    std::vector<Texture> loadMaterialTextures(aiMaterial* mat, aiTextureType type, std::string typeName)
    {
        std::vector<Texture> textures;
        for(GLuint i = 0; i < mat->GetTextureCount(type); i++)
        {
            aiString str;
            mat->GetTexture(type, i, &str);
            // Check if texture was loaded before and if so, continue to next iteration: skip loading a new texture
            GLboolean skip = false;
            for(GLuint j = 0; j < textures_loaded.size(); j++)
            {
                if(textures_loaded[j].path == str)
                {
                    textures.push_back(textures_loaded[j]);
                    skip = true; // A texture with the same filepath has already been loaded, continue to next one. (optimization)
                    break;
                }
            }
            if(!skip)
            {   // If texture hasn't been loaded already, load it
                Texture texture;
                texture.id = TextureFromFile(str.C_Str(), this->directory);
                texture.type = typeName;
                texture.path = str;
                textures.push_back(texture);
                this->textures_loaded.push_back(texture);  // Store it as texture loaded for entire model, to ensure we won't unnecesery load duplicate textures.
            }
        }
        return textures;
    }
};




GLint TextureFromFile(const char* path, std::string directory)
{
     //Generate texture ID and load texture data 
    std::string filename = std::string(path);
    filename = directory + '/' + filename;
    GLuint textureID;
    glGenTextures(1, &textureID);
    int width,height, components;
    unsigned char* image = stbi_load(filename.c_str(), &width, &height, &components, 0);
    // Assign texture to ID
    glBindTexture(GL_TEXTURE_2D, textureID);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image);
    glGenerateMipmap(GL_TEXTURE_2D);	

    // Parameters
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT );
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT );
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR );
    glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glBindTexture(GL_TEXTURE_2D, 0);
    stbi_image_free(image);
    return textureID;
}

/*

	void renderSoftbodyMeshes(btSoftBody* sBody)
	{
		btTransform meshTransform = sBody->getWorldTransform();

		this->textures_loaded.at(0).path;

		int j = 0;

		static btScalar tempForm[16];
		meshTransform.getOpenGLMatrix(tempForm);

		GLuint imageData = this->textures_loaded.at(0).id;
		int width, height, components;
		unsigned char* image = stbi_load(this->textures_loaded.at(0).path.C_Str(), &width, &height, &components, 0);

		glBindTexture(GL_TEXTURE_2D, imageData);
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image);
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP);
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP);

		glPushMatrix();
		glMultMatrixf(tempForm);
		glBegin(GL_TRIANGLES);
		int numFaces = sBody->m_faces.size();
		for (int i = 0; i < numFaces; i++)
		{
			glNormal3fv(sBody->m_faces.at(i).m_n[0]->m_n);
			glTexCoord2fv(&this->meshes.at(0).vertices.at(0).TexCoords[this->meshes.at(0).indices[0]]);
			glVertex3fv(sBody->m_faces.at(i).m_n[0]->m_q);

			glNormal3fv(sBody->m_faces.at(i).m_n[1]->m_n);
			glTexCoord2fv(&this->meshes.at(0).vertices.at(0).TexCoords[this->meshes.at(0).indices[0]]);
			glVertex3fv(sBody->m_faces.at(i).m_n[1]->m_q);

			glNormal3fv(sBody->m_faces.at(i).m_n[2]->m_n);
			glTexCoord2fv(&this->meshes.at(0).vertices.at(0).TexCoords[this->meshes.at(0).indices[0]]);
			glVertex3fv(sBody->m_faces.at(i).m_n[2]->m_q);
		}

		glEnd();
		glPopMatrix();

		glDisable(GL_TEXTURE_2D);
	}
*/