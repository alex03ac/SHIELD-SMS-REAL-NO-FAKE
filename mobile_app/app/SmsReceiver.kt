package com.af.shieldsms

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import com.squareup.moshi.Moshi
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor

data class ClassifyRequest(val message: String)
data class ClassifyResponse(val label: String, val score: Double)

interface ApiService {
    @retrofit2.http.POST("/classify")
    suspend fun classify(@retrofit2.http.Body b: ClassifyRequest): Response<ClassifyResponse>
}

private fun api(): ApiService {
    val log = HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
    val client = OkHttpClient.Builder().addInterceptor(log).build()
    val rt = Retrofit.Builder()
        .baseUrl(BuildConfig.BASE_URL)
        .client(client)
        .addConverterFactory(MoshiConverterFactory.create(Moshi.Builder().build()))
        .build()
    return rt.create(ApiService::class.java)
}

class SmsReceiver : BroadcastReceiver() {
    override fun onReceive(ctx: Context, intent: Intent) {
        if (intent.action != Telephony.Sms.Intents.SMS_RECEIVED_ACTION) return
        val msgs = Telephony.Sms.Intents.getMessagesFromIntent(intent)
        val body = msgs.joinToString(" ") { it.messageBody ?: "" }
        Log.d("ShieldSMS", "SMS: $body")

        // Llamada simple al backend (MVP)
        val pr = goAsync()
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val resp = api().classify(ClassifyRequest(body))
                if (resp.isSuccessful) {
                    Log.d("ShieldSMS", "OK: ${resp.body()}")
                } else {
                    Log.e("ShieldSMS", "HTTP ${resp.code()}")
                }
            } catch (e: Exception) {
                Log.e("ShieldSMS", "Error", e)
            } finally { pr.finish() }
        }
    }
}
