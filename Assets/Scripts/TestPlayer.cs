using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestPlayer: MonoBehaviour
{
    float speed = 5.0f;
    // add more sound effect in feedbackAudioList if you want
    AudioSource[] audioSources;
    AudioSource feedbackAudioSource;
    public List<AudioClip> feedbackAudioList = new List<AudioClip>();

    AudioClip tempAudioClip;
    void Start()
    {
        speed = 5.0f;
        audioSources = GetComponents<AudioSource>();
        feedbackAudioSource= audioSources[0];
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            transform.Translate(Vector3.forward * Time.deltaTime * speed);
        }
        if (Input.GetKey(KeyCode.S))
        {
            transform.Translate(-1 * Vector3.forward * Time.deltaTime * speed);
        }
        if (Input.GetKey(KeyCode.A))
        {
            transform.Rotate(0, -1, 0);
        }
        if (Input.GetKey(KeyCode.D))
        {
            transform.Rotate(0, 1, 0);
        }

    }

   // Here I only provide 
    private void OnCollisionEnter(Collision collision)
    {
        if(collision.gameObject.tag == "Wall")
        {
            Debug.Log("Wall Hit");
            feedbackAudioSource.PlayOneShot(feedbackAudioList[0], 1); 
        }
       else if(collision.gameObject.tag == "Hydrant")
        {
            Debug.Log("Hydrant Hit");
            feedbackAudioSource.PlayOneShot(feedbackAudioList[1], 1);
        }
       else if(collision.gameObject.tag == "Ramp")
        {
            Debug.Log("Ramp Hit");
            feedbackAudioSource.PlayOneShot(feedbackAudioList[2], 1);
        }
        else if(collision.gameObject.tag == "Tree")
        {
            Debug.Log("Tree Hit");
            feedbackAudioSource.PlayOneShot(feedbackAudioList[3], 1);
        }
    }


}
